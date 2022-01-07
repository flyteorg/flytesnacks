House Price Regression
-----------------------

House Price Regression refers to the prediction of house prices based on various factors, using the XGBoost Regression model (in our case).
In this example, we will train our data on the XGBoost model to predict house prices in multiple regions.

Generally, this can be accomplished using any regression model in Machine Learning.

.. _flyte's-role:

Where does Flyte fit in?
==========================
- Orchestrates the machine learning pipeline.
- Helps cache the output state between the steps (tasks as per Flyte).
- Easier backtracking to the error source.
- Provides a Rich UI (if the Flyte backend is enabled) to view and manage the pipeline.

A typical house price prediction model isn’t dynamic, but a task has to be dynamic when multiple regions are involved. 

To learn more about dynamic workflows, refer to `Write a dynamic task <https://docs.flyte.org/projects/cookbook/en/latest/auto/core/control_flow/dynamics.html#dynamic-workflows>`__.

Dataset
========
There is no built-in dataset that could be employed to build this model. A dataset will have to be created, possibly using this reference model on `Github <https://github.com/awslabs/amazon-sagemaker-examples/blob/master/advanced_functionality/multi_model_xgboost_home_value/xgboost_multi_model_endpoint_home_value.ipynb>`__.

The dataset will have the following columns:

- Price

- House Size

- Number of Bedrooms

- Year Built

- Number of Bathrooms

- Number of Garage Spaces

- Lot Size

Steps to Build the Machine Learning Pipeline
==============================================
- Generate the dataset, and split it into train, validation, and test subsets
- Fit the XGBoost model to the data
- Generate predictions

Steps to Make the Pipeline Flyte-Compatible
=============================================
- Create two Python files to segregate the house price prediction logic. One consists of the logic per region, and the other one works for multiple regions.
- Define a couple of helper functions that will be used while defining Flyte tasks and workflows.
- Define three Flyte tasks -- 
	1. to generate and split the data;
	2. fit the model;
	3. generate predictions;
- If there are multiple regions, the tasks are `dynamic <https://docs.flyte.org/projects/cookbook/en/latest/auto/core/control_flow/dynamics.html#dynamic-workflows>`__ in nature.
- Define a workflow to call the dynamic tasks in a specified order.

Takeaways
===========
- An in-depth dive into dynamic workflows
- How the Flyte type-system works

Code Walkthrough
==================
