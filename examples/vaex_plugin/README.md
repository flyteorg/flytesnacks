
# Vaex

```{eval-rst}
.. tags:: Integration, DataFrame, MachineLearning, Intermediate
```

[Vaex](https://vaex.io) is a Big Data/Dataframe package as a partial Pandas replacement. It uses lazy evaluation and memory mapping to allow users work with big data on their daily standard machines. Supports more than 100+ gigabytes of dataframes for easy explorations and visualizations. 

The Flytekit Vaex plugin leverages the efficient Exploratory Data Analysis on big data within your workflow.

## Installation 

To install the Flytekit Vaex plugin, run the following command:

```
pip install flytekitplugins-vaex
```

The Flytekit Vaex plugin includes the {py:class}`~flytekitplugins:flytekitplugins.Vaex.VaexDataframe` as Data type with `StructuredDataset`, which allows you to utilize Vaex big data support.

## How is Vaex different?

While Modin and other alternatives trying to fully compatibility with Pandas, Vaex is a partial Pandas replacement that aims more on the Big Dataframes Visualizations and Explorations! 

```{auto-examples-toc}
vaex_example
```
