Example of a MultiStep Linear Workflow
======================================

Introduction:
-------------
The workflow is a simple multistep xgboost trainer. 
- Step1: Gather data and split it into training and validation sets
- Step2: Fit the actual model
- Step3: Run a set of predictions on the validation set. The function is designed to be more generic, it can be used to simply predict given a set of observations (dataset)
- Step4: Calculate the accuracy score for the predictions

The workflow is designed for a dataset as defined in 
https://github.com/jbrownlee/Datasets/blob/master/pima-indians-diabetes.names

An example dataset is available at
https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv

Important things to note:
-------------------------
- Usage of Schema Type. Schema type allows passing a type safe row vector from one task to task. The row vector is also directly loaded into a pandas dataframe
  We could use an unstructured Schema (By simply omiting the column types). this will allow any data to be accepted by the train algorithm.

- We pass the file as a CSV input. The file is auto-loaded.

