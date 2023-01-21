---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting_started_visualizing_artifacts)=

# Visualizing Artifacts

Flyte {py:class}`~flytekit.deck.Deck`s are one of the first-class constructs in
Flyte, allowing you to generate static HTML reports associated any of the
artifacts associated with your tasks.

You can think of Decks as stacks of HTML snippets that are logically grouped.
By default, every task has three decks: an **input**, an **output**, and a
**default** deck.

Flyte materializes Decks via renderers, which are specific implementations of
how to generate an HTML report from some Python object.

## Enabling Flyte Decks

To enable Flyte Decks, simply set `disable_deck=False` in the `@task` decorator:


```{code-cell} ipython3
import pandas as pd
from flytekit import task, workflow


@task(disable_deck=False)
def iris_data() -> pd.DataFrame:
    ...
```

Specifying this flag indicates that Decks should be rendered whenever this task
is invoked.


## Rendering Task Inputs and Outputs

By default, Flyte will render the inputs and outputs of tasks with the built-in
renderers in the corresponding **input** and **output** decks, respectively.
In the following task, we load the iris dataset using the `plotly` package.

```{code-cell} ipython3

import plotly.express as px
from typing import Optional

from flytekit import task, workflow


@task(disable_deck=False)
def iris_data(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
) -> pd.DataFrame:
    data = px.data.iris()
    if sample_frac is not None:
        data = data.sample(frac=sample_frac, random_state=random_state)
    return data


@workflow
def wf(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
):
    iris_data(sample_frac=sample_frac, random_state=random_state)
```

Then, invoking the workflow containing a deck-enabled task will render the
following reports for the input and output data:


```{code-cell} ipython3
---
tags: [remove-input]
---

# this is an unrendered cell, used to capture the logs in order to render the
# Flyte Decks directly in the docs.
import logging
import os
import re
from IPython.display import HTML, IFrame


class DeckFilter(logging.Filter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deck_files = {}
    
    def filter(self, record):
        patt = "(.+) task creates flyte deck html to (.+/deck.html)"
        matches = re.match(patt, record.getMessage())
        if matches:
            task, filepath = matches.group(1), matches.group(2)
            self.deck_files[task] = re.sub("^file://", "", filepath)
        return True


logger = logging.getLogger("flytekit")
logger.setLevel(20)

deck_filter = DeckFilter()
logger.addFilter(deck_filter)
```

```{code-cell} ipython3
wf(sample_frac=1.0, random_state=42)
```

As you can see below, the built-in decks for the **input** arguments for
primitive types like `int` and `float` are barebones, simply showing the
values. The **output** argument in this case is a `pandas.DataFrame`, where
the default renderer will display the first and last five rows.

```{code-cell} ipython3
---
tags: [remove-input]
---

import os
import shutil
from pathlib import Path

def cp_deck(src):
    src = Path(src)
    target = Path.cwd() / ".." / "_flyte_decks" / src.parent.name
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, target)
    return target / "deck.html"

logger.removeFilter(deck_filter)
IFrame(src=cp_deck(deck_filter.deck_files["iris_data"]), width="100%", height="400px")
```

````{note}
To see where the HTML file is written to when you run the deck-enabled tasks
locally, you need to set the `FLYTE_SDK_LOGGING_LEVEL` environment variable
to `20`. Doing so will emit logs that look like:


```{code-block}
{"asctime": "2023-01-18 17:48:55,722", "name": "flytekit", "levelname": "INFO", "message": "iris_data task creates flyte deck html to file:///var/folders/4q/frdnh9l10h53gggw1m59gr9m0000gn/T/flyte-mq3hz60r/sandbox/local_flytekit/a8278eb21300b63504d9a4d5a4b41ca2/deck.html"}
```

Where the `deck.html` filepath can be found in the `message` key.
````

## Rendering In-line Decks

You can render Decks inside the task function body by using the **default**
deck, which you can access with the {py:func}`~flytekit.current_context`
function. In the following example, we extend the `iris_data` task with:

- A markdown snippet to provide more context about what the task does.
- A profile of the dataset using the {py:class}`~flytekitplugins.deck.FrameProfilingRenderer`,
  which leverages the [`pandas-profiling`](https://pandas-profiling.ydata.ai/docs/master/index.html)
  package to auto-generate a set of plots and summary statistics from the dataframe.

```{code-cell} ipython
import flytekit
from flytekitplugins.deck.renderer import MarkdownRenderer, FrameProfilingRenderer

@task(disable_deck=False)
def iris_data(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
) -> pd.DataFrame:
    data = px.data.iris()
    if sample_frac is not None:
        data = data.sample(frac=sample_frac, random_state=random_state)

    md_text = (
        "# Iris Dataset\n"
        "This task loads the iris dataset using the  `plotly` package."
    )
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    flytekit.Deck("profile", FrameProfilingRenderer("Iris").to_html(data))
    return data
```

Re-running the workflow, we get:

```{code-cell} ipython
---
tags: [remove-input]
---
import warnings

@workflow
def wf(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
):
    iris_data(sample_frac=sample_frac, random_state=random_state)

deck_filter = DeckFilter()
logger.addFilter(deck_filter)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    wf(sample_frac=1.0, random_state=42)

logger.removeFilter(deck_filter)
IFrame(src=cp_deck(deck_filter.deck_files["iris_data"]), width="100%", height="400px")
```

## Custom Renderers

What if we don't want to show raw data values in the Flyte Deck? We can create a
pandas dataframe renderer that summarizes the data instead of showing raw values
by creating a custom renderer. A renderer is essentially a class with a
`to_html` method.

```{code-cell} ipython
class DataFrameSummaryRenderer:

    def to_html(self, df: pd.DataFrame) -> str:
        assert isinstance(df, pd.DataFrame)
        return df.describe().to_html()
```

Then we can use the `Annotated` type to override the default renderer of the
`pandas.DataFrame` type:

```{code-cell} ipython
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


@task(disable_deck=False)
def iris_data(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
) -> Annotated[pd.DataFrame, DataFrameSummaryRenderer()]:
    data = px.data.iris()
    if sample_frac is not None:
        data = data.sample(frac=sample_frac, random_state=random_state)

    md_text = (
        "# Iris Dataset\n"
        "This task loads the iris dataset using the  `plotly` package."
    )
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    return data
```

Running this version of our `iris_data` task, we get the Deck below. Go to the
**output** tab to see that the dataset is rendered as a summary table instead of
the first and last few rows of the actual data.

```{code-cell} ipython
---
tags: [remove-input]
---
import warnings

@workflow
def wf(
    sample_frac: Optional[float] = None,
    random_state: Optional[int] = None,
):
    iris_data(sample_frac=sample_frac, random_state=random_state)

deck_filter = DeckFilter()
logger.addFilter(deck_filter)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    wf(sample_frac=1.0, random_state=42)

logger.removeFilter(deck_filter)
IFrame(src=cp_deck(deck_filter.deck_files["iris_data"]), width="100%", height="400px")
```

As we can see from the `DataFrameSummaryRenderer` example above, Flyte Decks
are simple to customize, as long as you can render the Python object into some
HTML representation.

```{note}
Learn more about Flyte Decks in the {ref}`User Guide <flyte-decks>`.
```

## What's Next?

In this guide, you learned how to generate static HTML reports to gain more
visibility into Flyte tasks. In the next guide, you'll learn how to optimize
your tasks via caching, retries, parallelization, resource allocation, and
plugins.
