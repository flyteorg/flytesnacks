"""
Flyte decks
-------------

Deck enable users to get customizable and default visibility into their tasks.

Deck contains a list of renderers (FrameRenderer, MarkdownRenderer) that can
generate a html file. For example, FrameRenderer can render a DataFrame as an HTML table,
MarkdownRenderer can convert Markdown string to HTML

Each task has a least three decks (input, output, default). Input/output decks are
used to render tasks' input/output data, and the default deck is used to render line plots,
scatter plots or markdown text. In addition, users can create new decks to render
their data with custom renderers.
"""
import pandas as pd
import plotly.express as px
from flytekitplugins.deck.renderer import BoxRenderer, MarkdownRenderer
from typing_extensions import Annotated

import flytekit
from flytekit import task, workflow
from flytekit.deck.renderer import TopFrameRenderer

iris_df = px.data.iris()


# %
# Here we first create new deck called demo, and use box renderer to show box plot on demo deck.
# Then use MarkdownRenderer to render md_text, and append HTML to default deck.
@task()
def t1() -> str:
    md_text = "#Hello Flyte\n##Hello Flyte\n###Hello Flyte"
    flytekit.Deck("demo", BoxRenderer("sepal_length").to_html(iris_df))
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    return md_text


"""
Expected output:

.. prompt:: text

  {"asctime": "2022-04-19 23:12:17,266", "name": "flytekit", "levelname": "INFO", "message": "t1 output flytekit deck html to file:///tmp/flyte/20220419_231216/sandbox/local_flytekit/161e15f8c9331e83237bcf52e604697b/deck.html"}
  {"asctime": "2022-04-19 23:12:17,283", "name": "flytekit", "levelname": "INFO", "message": "t2 output flytekit deck html to file:///tmp/flyte/20220419_231216/sandbox/local_flytekit/6d8d1bafe04769592d7b0e212c50bd0e/deck.html"}

"""

# %
# .. figure:: https://keep.google.com/u/0/media/v2/18EI0XAdBEHTFiHAIKX5vG_crQp7wOVIR1zPFDeFVhV-An87zi4-VNaOn-O3VzQ/1J-nKZvxl0U9ZPRBis9gJGt19y4wfasOucImobO74zzICnwP3s8kztijpd7abON4?sz=512&accept=image%2Fgif%2Cimage%2Fjpeg%2Cimage%2Fjpg%2Cimage%2Fpng%2Cimage%2Fwebp
#   :alt: Demo Deck
#   :class: with-shadow
#
#   Demo Deck
# .. figure:: https://keep.google.com/u/0/media/v2/1OWpuyWk_udxUp1Qu12EAJotuJLGjq9ygyTTZcpP3FyRpalpSOKiEsLOUHe01ZA/1o3ccc_6NQ6v3cqzf0Z2l5Z54nL4BrP6mM0TvVCX9CMPXaIy-BmwI6C3JwnzB1w?sz=512&accept=image%2Fgif%2Cimage%2Fjpeg%2Cimage%2Fjpg%2Cimage%2Fpng%2Cimage%2Fwebp
#   :alt: Default Deck
#   :class: with-shadow
#
#   Default Deck


# %
# Use Annotated to override default renderer, and display top 10 rows of dataframe
@task()
def t2() -> Annotated[pd.DataFrame, TopFrameRenderer(10)]:
    return iris_df

# %
# .. figure:: https://keep.google.com/u/0/media/v2/17Gzd6gM-EaionxXzwDZvXeMt3d4l69YPN-ubR3Mp2RSKoIDUOZvF3DTTmZPA6vQ/1DXoZXSh4NlRZ7XBCuc7tGlYk2tLdOiuWI-YjuH7MCEs3FSiDc4OCg4kX36Dixw?sz=512&accept=image%2Fgif%2Cimage%2Fjpeg%2Cimage%2Fjpg%2Cimage%2Fpng%2Cimage%2Fwebp
#   :alt: Output Deck
#   :class: with-shadow
#
#   Output Deck


@workflow
def wf():
    t1()
    t2()


if __name__ == "__main__":
    wf()
