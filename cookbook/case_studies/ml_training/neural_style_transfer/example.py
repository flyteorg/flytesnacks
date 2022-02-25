import os
from typing import Tuple

import flytekit
import numpy as np
import PIL.Image
import tensorflow as tf
from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import FlyteFile

style_weight = 1e-2
content_weight = 1e4
total_variation_weight = 30

# Load compressed models from tensorflow_hub
os.environ["TFHUB_MODEL_LOAD_FORMAT"] = "COMPRESSED"

content_layers = ["block5_conv2"]
style_layers = [
    "block1_conv1",
    "block2_conv1",
    "block3_conv1",
    "block4_conv1",
    "block5_conv1",
]

request_resources = Resources(cpu="1", mem="500Mi", storage="500Mi")


@task(requests=request_resources)
def tensor_to_image(tensor: tf.Variable) -> FlyteFile:
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    working_dir = flytekit.current_context().working_directory
    image_path = os.path.join(working_dir, "neural_style_transferred_img.png")
    image = PIL.Image.fromarray(tensor)
    image.save(image_path)
    return image_path


def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


@task(requests=request_resources)
def preprocess_images(
    content_img: FlyteFile, style_img: FlyteFile
) -> Tuple[tf.Tensor, tf.Tensor]:
    content_path = content_img.download()
    style_path = style_img.download()

    content_image = load_img(content_path)
    style_image = load_img(style_path)

    return content_image, style_image


def vgg_layers(layer_names):
    """Creates a vgg model that returns a list of intermediate output values."""
    # Load our model. Load pretrained VGG, trained on imagenet data
    vgg = tf.keras.applications.VGG19(include_top=False, weights="imagenet")
    vgg.trainable = False

    outputs = [vgg.get_layer(name).output for name in layer_names]

    model = tf.keras.Model([vgg.input], outputs)
    return model


def gram_matrix(input_tensor):
    result = tf.linalg.einsum("bijc,bijd->bcd", input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
    return result / (num_locations)


class StyleContentModel(tf.keras.models.Model):
    def __init__(self, style_layers, content_layers):
        super(StyleContentModel, self).__init__()
        self.vgg = vgg_layers(style_layers + content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.vgg.trainable = False

    def call(self, inputs):
        "Expects float input in [0,1]"
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (
            outputs[: self.num_style_layers],
            outputs[self.num_style_layers :],
        )

        style_outputs = [gram_matrix(style_output) for style_output in style_outputs]

        content_dict = {
            content_name: value
            for content_name, value in zip(self.content_layers, content_outputs)
        }

        style_dict = {
            style_name: value
            for style_name, value in zip(self.style_layers, style_outputs)
        }

        return {"content": content_dict, "style": style_dict}


def clip_0_1(image):
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def style_content_loss(outputs, content_targets, style_targets):
    style_outputs = outputs["style"]
    content_outputs = outputs["content"]
    style_loss = tf.add_n(
        [
            tf.reduce_mean((style_outputs[name] - style_targets[name]) ** 2)
            for name in style_outputs.keys()
        ]
    )
    style_loss *= style_weight / len(style_layers)

    content_loss = tf.add_n(
        [
            tf.reduce_mean((content_outputs[name] - content_targets[name]) ** 2)
            for name in content_outputs.keys()
        ]
    )
    content_loss *= content_weight / len(content_layers)
    loss = style_loss + content_loss
    return loss


@task(requests=request_resources)
def train_step(
    image: tf.Variable, content_image: tf.Tensor, style_image: tf.Tensor
) -> tf.Variable:
    opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)
    extractor = StyleContentModel(style_layers, content_layers)

    style_targets = extractor(style_image)["style"]
    content_targets = extractor(content_image)["content"]

    with tf.GradientTape() as tape:
        outputs = extractor(image)
        loss = style_content_loss(outputs, content_targets, style_targets)
        loss += total_variation_weight * tf.image.total_variation(image)

    grad = tape.gradient(loss, image)
    opt.apply_gradients([(grad, image)])
    image.assign(clip_0_1(image))

    return image


@dynamic(
    requests=Resources(cpu="1", mem="5Gi", storage="5Gi", ephemeral_storage="500Mi")
)
def generate_image(
    content_image: tf.Tensor, style_image: tf.Tensor, epochs: int, steps_per_epoch: int
) -> FlyteFile:
    image = tf.Variable(content_image)

    step = 0
    for n in range(epochs):
        for m in range(steps_per_epoch):
            step += 1
            image = train_step(
                image=image, content_image=content_image, style_image=style_image
            )
            print(".", end="", flush=True)
        print("Train step: {}".format(step))

    return tensor_to_image(tensor=image)


@workflow
def neural_style_transfer_wf(
    content_img: FlyteFile = "https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg",
    style_img: FlyteFile = "https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg",
    epochs: int = 10,
    steps_per_epoch: int = 100,
) -> FlyteFile:
    content_image, style_image = preprocess_images(
        content_img=content_img, style_img=style_img
    )
    return generate_image(
        content_image=content_image,
        style_image=style_image,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
    )


if __name__ == "__main__":
    print(f"Running {__file__}...")
    print(f"Image after styles have been transferred: {neural_style_transfer_wf()}")
