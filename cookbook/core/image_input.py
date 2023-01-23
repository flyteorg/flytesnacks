import typing
from random import random
from datetime import timedelta

from flytekit import wait_for_input, task, workflow, current_context
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.datasets import load_digits
import numpy
from io import BytesIO
import base64


class MatplotFigureRenderer(object):
    def to_html(self, fig: Figure) -> str:
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return f"<img src='data:image/png;base64,{encoded}'>"


@task(disable_deck=False)
def plot_images() -> numpy.ndarray:  # noqa
    data = load_digits()
    X = data.images.reshape(len(data.images), -1)[68:88]

    fig = plt.figure(figsize=(20, 4))
    for index, image in enumerate(X[0:20]):
        plt.subplot(1, 20, index + 1)
        plt.imshow(np.reshape(image, (8, 8)), cmap=plt.cm.gray)
        plt.title('Training: %in' % index, fontsize=15)

    d = current_context().default_deck
    d.append(MatplotFigureRenderer().to_html(fig))

    return X


@task
def validate_model(known_values: typing.List[int], data: numpy.ndarray) -> float:
    print(f"Known values are {known_values}")
    print(f"Data: {data}")
    model_score = random()
    print(f"Score: {model_score}")
    return model_score


@workflow
def wf() -> float:
    image_data = plot_images()
    s1 = wait_for_input("images-values-known", timeout=timedelta(hours=1), expected_type=typing.List[int])
    score = validate_model(known_values=s1, data=image_data)
    return score



