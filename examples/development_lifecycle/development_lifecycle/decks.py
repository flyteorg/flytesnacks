import flytekit
from flytekit import ImageSpec, task
from flytekit.deck.renderer import MarkdownRenderer
from sklearn.decomposition import PCA

# Create a new deck named `pca` and render Markdown content along with a
# PCA (https://en.wikipedia.org/wiki/Principal_component_analysis) plot.
# Start by initializing an `ImageSpec`` object
# to encompass all the necessary dependencies.
# This approach automatically triggers a Docker build,
# alleviating the need for you to manually create a Docker image.
# For more information, see
# https://docs.flyte.org/en/latest/user_guide/customizing_dependencies/imagespec.html#image-spec-example

custom_image = ImageSpec(
    packages=["plotly", "scikit-learn", "flytekitplugins-deck-standard"], registry="ghcr.io/flyteorg"
)

if custom_image.is_container():
    import plotly
    import plotly.express as px


# Note the usage of `append` to append the Plotly deck to the Markdown deck
@task(enable_deck=True, container_image=custom_image)
def pca_plot():
    iris_df = px.data.iris()
    X = iris_df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    pca = PCA(n_components=3)
    components = pca.fit_transform(X)
    total_var = pca.explained_variance_ratio_.sum() * 100
    fig = px.scatter_3d(
        components,
        x=0,
        y=1,
        z=2,
        color=iris_df["species"],
        title=f"Total Explained Variance: {total_var:.2f}%",
        labels={"0": "PC 1", "1": "PC 2", "2": "PC 3"},
    )
    main_deck = flytekit.Deck("pca", MarkdownRenderer().to_html("### Principal Component Analysis"))
    main_deck.append(plotly.io.to_html(fig))


# Frame renderer creates a profile report from a Pandas DataFrame.
import pandas as pd
from flytekitplugins.deck.renderer import FrameProfilingRenderer


@task(enable_deck=True)
def frame_renderer() -> None:
    df = pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
    flytekit.Deck("Frame Renderer", FrameProfilingRenderer().to_html(df=df))


# Top-frame renders DataFrame as an HTML table.
# This renderer doesn't necessitate plugin installation since it's accessible
# within the flytekit library.
from typing import Annotated

from flytekit.deck import TopFrameRenderer


@task(enable_deck=True)
def top_frame_renderer() -> Annotated[pd.DataFrame, TopFrameRenderer(1)]:
    return pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})


# Markdown renderer converts a Markdown string into HTML,
# producing HTML as a Unicode string.


@task(enable_deck=True)
def markdown_renderer() -> None:
    flytekit.current_context().default_deck.append(
        MarkdownRenderer().to_html("You can install flytekit using this command: ```import flytekit```")
    )


# Box renderer groups rows of DataFrame together into a
# box-and-whisker mark to visualize their distribution.
#
# Each box extends from the first quartile (Q1) to the third quartile (Q3).
# The median (Q2) is indicated by a line within the box.
# Typically, the whiskers extend to the edges of the box,
# plus or minus 1.5 times the interquartile range (IQR: Q3-Q1).
from flytekitplugins.deck.renderer import BoxRenderer


@task(enable_deck=True)
def box_renderer() -> None:
    iris_df = px.data.iris()
    flytekit.Deck("Box Plot", BoxRenderer("sepal_length").to_html(iris_df))


# Image renderer converts a {ref}`FlyteFile <files>` or `PIL.Image.Image`
# object into an HTML string,
# where the image data is encoded as a base64 string.
from flytekit import workflow
from flytekit.types.file import FlyteFile
from flytekitplugins.deck.renderer import ImageRenderer


@task(enable_deck=True)
def image_renderer(image: FlyteFile) -> None:
    flytekit.Deck("Image Renderer", ImageRenderer().to_html(image_src=image))


@workflow
def image_renderer_wf(
    image: FlyteFile = "https://bit.ly/3KZ95q4",
) -> None:
    image_renderer(image=image)


# Table renderer converts a Pandas dataframe into an HTML table.
from flytekitplugins.deck.renderer import TableRenderer


@task(enable_deck=True)
def table_renderer() -> None:
    flytekit.Deck(
        "Table Renderer",
        TableRenderer().to_html(df=pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]}), table_width=50),
    )
