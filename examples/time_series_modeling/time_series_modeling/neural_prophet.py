# %% [markdown]
# # Train a Neural Prophet Model
#
# This script demonstrates how to train a model for time series forecasting
# using the [neural prophet](https://neuralprophet.com/) library.

# %% [markdown]
# ## Imports and Setup
#
# First, we import necessary libraries to run the training workflow.

import pandas as pd
from flytekit import Deck, ImageSpec, current_context, task, workflow
from flytekit.types.file import FlyteFile

# %% [markdown]
# ## Define an ImageSpec
#
# For reproducibility, we create an `ImageSpec` object with required packages
# for our tasks.

image = ImageSpec(
    name="neuralprophet",
    packages=[
        "neuralprophet",
        "matplotlib",
        "ipython",
        "pandas",
        "pyarrow",
    ],
    # This registry is for a local flyte demo cluster. Replace this with your
    # own registry, e.g. `docker.io/<username>/<imagename>`
    registry="localhost:30000",
)

# %% [markdown]
# ## Data Loading Task
#
# This task loads the time series data from the specified URL. In this case,
# we use a hard-coded URL for a sample dataset that ships with the neural prophet.

URL = "https://github.com/ourownstory/neuralprophet-data/raw/main/kaggle-energy/datasets/tutorial01.csv"


@task(container_image=image)
def load_data() -> pd.DataFrame:
    return pd.read_csv(URL)


# %% [markdown]
# ## Model Training Task
#
# This task trains the Neural Prophet model on the loaded data.
# We train the model in the hourly frequency for ten epochs.


@task(container_image=image)
def train_model(df: pd.DataFrame) -> FlyteFile:
    from neuralprophet import NeuralProphet, save

    working_dir = current_context().working_directory
    model = NeuralProphet()
    model.fit(df, freq="H", epochs=10)
    model_fp = f"{working_dir}/model.np"
    save(model, model_fp)
    return FlyteFile(model_fp)


# %% [markdown]
# ## Forecasting Task
#
# This task loads the trained model, makes predictions, and visualizes the
# results using a Flyte Deck.


@task(
    container_image=image,
    enable_deck=True,
)
def make_forecast(df: pd.DataFrame, model_file: FlyteFile) -> pd.DataFrame:
    from neuralprophet import load

    model_file.download()
    model = load(model_file.path)

    # Create a new dataframe reaching 365 days into the future
    # for our forecast, n_historic_predictions also shows historic data
    df_future = model.make_future_dataframe(
        df,
        n_historic_predictions=True,
        periods=365,
    )

    # Predict the future
    forecast = model.predict(df_future)

    # Plot on a Flyte Deck
    fig = model.plot(forecast)
    Deck("Forecast", fig.to_html())

    return forecast


# %% [markdown]
# ## Main Workflow
#
# Finally, this workflow orchestrates the entire process: loading data,
# training the model, and making forecasts.


@workflow
def main() -> pd.DataFrame:
    df = load_data()
    model_file = train_model(df)
    forecast = make_forecast(df, model_file)
    return forecast
