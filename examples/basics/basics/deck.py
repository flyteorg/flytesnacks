# %% [markdown]
# (flyte-decks)=
#
# # Flyte Decks
#
# ```{eval-rst}
# .. tags:: UI, Basic
# ```
#
# The Deck feature enables you to obtain customizable and default visibility into your tasks.
#
# Flytekit contains various renderers such as FrameRenderer and MarkdownRenderer, which generate HTML files.
# For instance, FrameRenderer renders a DataFrame as an HTML table, while MarkdownRenderer converts Markdown strings to HTML.
#
# Each task has a minimum of three decks: input, output and default.
# The input/output decks are used to render the input/output data of tasks, while the default deck can be used to render line plots, scatter plots or markdown text.
# Additionally, you can create new decks to render your data using custom renderers.
#
# Now, let's dive into an example.
# %% [markdown]
# :::{note}
# Flyte Decks is an opt-in feature; to enable it, set `disable_deck` to `False` in the task params.
# :::

# %% [markdown]
# First, import the dependencies.
# %%
import flytekit
from flytekit import ImageSpec, task
from flytekitplugins.deck.renderer import MarkdownRenderer
from sklearn.decomposition import PCA

# %% [markdown]
# Create a new deck called `pca` and render markdown content along with the PCA plot.
#
# Initialize `ImageSpec` object to capture all the dependencies required.
# This approach automatically triggers a Docker build, alleviating the need for you to manually create a Docker image.
#
# Note the usage of `append` to append the Plotly deck to the markdown deck.
# %%
custom_image = ImageSpec(name="flyte-decks-example", packages=["plotly"])

if custom_image.is_container():
    import plotly
    import plotly.express as px


@task(disable_deck=False, container_image=custom_image)
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


# %% [markdown]
# :::{Important}
# To view the log output locally, the `FLYTE_SDK_LOGGING_LEVEL` environment variable should be set to 20.
# :::

# %% [markdown]
# The following is the expected output containing the path to the deck.html file:
#
# ```{eval-rst}
# .. prompt:: text
#
# {"asctime": "2023-07-11 13:16:04,558", "name": "flytekit", "levelname": "INFO", "message": "pca_plot task creates flyte deck html to file:///var/folders/6f/xcgm46ds59j7g__gfxmkgdf80000gn/T/flyte-0_8qfjdd/sandbox/local_flytekit/c085853af5a175edb17b11cd338cbd61/deck.html"}
# ```

# %% [markdown]
# :::{figure} https://ik.imagekit.io/c8zl7irwkdda/flyte_decks?updatedAt=1689062089902
# :alt: Deck
# :class: with-shadow
# :::

# %% [markdown]
# :::{figure} https://i.ibb.co/7yCJnSs/flyteconsole.png
# :alt: FlyteConsole
# :class: with-shadow
# :::


# %% [markdown]
# ## Flyte Deck Renderer
#
# ### What Is a Flyte Deck Renderer?
#
# Deck renderer is a part of the Deck plugin. Deck provides default and customized task visibility. Deck contains renderers that generate HTML files.
# The renderer renders html in the [Flyte console](https://i.ibb.co/vhB8Mnz/dataframe.png), which can be used to visualize and document data associated with a task.
#
# Flyte context saves a list of deck objects, and these objects use renderers to render the data as HTML files when the task associated with it is executed.
#
# ### How to Use a Deck Renderer?
#
# You can render [custom data](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-deck-standard/flytekitplugins/deck/renderer.py) by creating [new decks](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-deck-standard/flytekitplugins/deck/renderer.py#L21-L30) and using custom renderers. The input to the renderer is your data and the output is a html string.
#
# Every task has a minimum of three decks:
#
# 1. Input deck;
# 2. Output deck; and
# 3. Default deck.
#
# The input and output decks render the input and output data associated with the task.
# The default deck renders line plots, scatter plots, and markdown text.
#
# ### How to Contribute Your Renderer?
#
# We would love any contributions to Flyte Deck. If your deck renderers can improve data visibility, feel free to add a renderer to [renderer.py](https://github.com/flyteorg/flytekit/blob/master/plugins/flytekit-deck-standard/flytekitplugins/deck/renderer.py). Feel free to open a pull request and help us enrich the Flyte Deck renderer ecosystem!
