---
next-page: ml_training
next-page-title: Model Training
---

(tutorials)=

# Tutorials

This section showcases step-by-step case studies of how to combine the different
features of Flyte to achieve everything from data processing, feature engineering,
model training, to batch predictions. Code for all of the examples in the user
guide can be found in the [flytesnacks](https://github.com/flyteorg/flytesnacks) repo.

It comes with a highly customized environment to make running, documenting and
contributing samples easy. If this is your first time running these examples, follow the
{ref}`setup guide <env_setup>` to get started.

```{note}
Want to contribute an example? Check out the {doc}`Example Contribution Guide <contribute>`.
```

## 🤖 Model Training

Train machine learning models from using your framework of choice.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Diabetes Classification <examples/pima_diabetes/README>`
  - Train an XGBoost model on the Pima Indians Diabetes Dataset.
* - {doc}`House Price Regression <examples/house_price_prediction/README>`
  - Use dynamic workflows to train a multiregion house price prediction model using XGBoost.
* - {doc}`MNIST Classification <examples/mnist_classifier/README>`
  - Train a neural network on MNIST with PyTorch and W&B
* - {doc}`NLP Processing with Gensim <examples/nlp_processing/README>`
  - Word embedding and topic modelling on lee background corpus with Gensim
* - {doc}`Sales Forecasting <examples/forecasting_sales/README>`
  - Use the Rossmann Store data to forecast sales with distributed training using Horovod on Spark.
```

## 🛠 Feature Engineering

Engineer the data features to improve your model accuracy.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`EDA and Feature Engineering With Papermill <examples/exploratory_data_analysis/README>`
  - How to use Jupyter notebook within Flyte
* - {doc}`Data Cleaning and Feature Serving With Feast <examples/feast_integration/README>`
  - How to use Feast to serve data in Flyte
```

## 🧪 Bioinformatics

Perform computational biology with Flyte.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Nucleotide Sequence Querying with BLASTX <examples/blast/README>`
  - Use BLASTX to Query a Nucleotide Sequence Against a Local Protein Database
```

## 🔬 Flytelab

The open-source repository of machine learning projects using Flyte.

```{list-table}
:header-rows: 0
:widths: 20 30

* - {doc}`Weather Forecasting <weather_forecasting>`
  - Build an online weather forecasting application.
```
