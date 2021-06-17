Data Cleaning
-------------
Feature Engineering off-late has become one of the most prominent topics in Machine Learning. 
It is the process of transforming raw data into features that better represent the underlying problem to the predictive models, resulting in improved model accuracy on unseen data.

This tutorial will implement data cleaning of SQLite3 data, which does both data imputation and univariate feature selection. These are so-called feature engineering techniques.

Where does Flyte fit in?
========================
Flyte provides a way to train models and perform feature engineering as a single pipeline.

Dataset
=======
We'll be using the horse colic dataset wherein we'll determine if the lesion of the horse was surgical or not. This is a modified version of the original dataset.

The dataset will have the following columns:

.. list-table:: Horse Colic Features
    :widths: 25 25 25

    * - surgery
      - Age
      - Hospital Number
    * - rectal temperature
      - pulse
      - respiratory rate
    * - temperature of extremities
      - peripheral pulse
      - mucous membranes
    * - capillary refill time
      - pain
      - peristalsis
    * - abdominal distension
      - nasogastric tube
      - nasogastric reflux
    * - nasogastric reflux PH
      - rectal examination
      - abdomen
    * - packed cell volume
      - total protein
      - abdominocentesis appearance
    * - abdomcentesis total protein
      - outcome
      - surgical lesion

The horse colic dataset will be a compressed zip file consisting of the SQLite DB.

Steps to Build the Pipeline
===========================
- Define two feature engineering tasks -- "data imputation" and "univariate feature selection"
- Reference the tasks in the actual file
- Define an SQLite3 Task and generate FlyteSchema
- Pass the inputs through an imperative workflow to validate the dataset
- Return the resultant DataFrame

Takeaways
=========
- Fetching the reference tasks
- Defining an imperative workflow
- Defining a shim task within an imperative workflow

Code Walkthrough
================
