import base64
import typing
from datetime import timedelta
from io import BytesIO
from random import random

import matplotlib.pyplot as plt
import numpy as np
from flytekit import current_context, task, wait_for_input, workflow
from matplotlib.figure import Figure
from sklearn.datasets import load_digits


class MatplotFigureRenderer(object):
    def to_html(self, fig: Figure) -> str:
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format="png")
        encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
        return f"<img src='data:image/png;base64,{encoded}'>"


@task(disable_deck=False)
def plot_images() -> np.ndarray:  # noqa
    data = load_digits()
    X = data.images.reshape(len(data.images), -1)[68:88]

    fig = plt.figure(figsize=(20, 4))
    for index, image in enumerate(X[0:20]):
        plt.subplot(1, 20, index + 1)
        plt.imshow(np.reshape(image, (8, 8)), cmap=plt.cm.gray)
        plt.title(f"{index}", fontsize=15)

    d = current_context().default_deck
    d.append(MatplotFigureRenderer().to_html(fig))

    return X


@task
def validate_model(labels: typing.List[int], data: np.ndarray) -> float:
    print(f"Known values are {labels}")
    print(f"Data: {data}")
    model_score = random()
    print(f"Score: {model_score}")
    return model_score


@workflow
def wf() -> float:
    image_data = plot_images()
    s1 = wait_for_input(
        "known-labels",
        timeout=timedelta(hours=1),
        expected_type=typing.List[int],
    )
    score = validate_model(labels=s1, data=image_data)
    return score
