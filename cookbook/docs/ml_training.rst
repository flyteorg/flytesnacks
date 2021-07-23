################
ML Training
################

.. panels::
    :header: text-center

    .. link-button:: auto/case_studies/ml_training/pima_diabetes/index
       :type: ref
       :text: Diabetes Classification
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Train an XGBoost model on the Pima Indians Diabetes Dataset

    ---

    .. link-button:: auto/case_studies/ml_training/house_price_prediction/index
       :type: ref
       :text: House Price Regression
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Use dynamic workflows to train a multiregion house price prediction model using XGBoost.

    ---

    .. link-button:: auto/case_studies/ml_training/pytorch/index
       :type: ref
       :text: PyTorch
       :classes: btn-block stretched-link
    ^^^^^^^^^^^^
    Train a Model Using PyTorch



.. toctree::
    :maxdepth: -1
    :caption: Contents
    :hidden:

    auto/case_studies/ml_training/pima_diabetes/index
    auto/case_studies/ml_training/house_price_prediction/index
    auto/case_studies/ml_training/pytorch/index


.. TODO: write tutorials for data parallel training, distributed training, and single node training

Run the following ``flytectl`` commands to execute your code (replace ``<code_directory>`` with the directory containing your code):

- Instantiate sandbox

.. prompt:: bash $

  flytectl sandbox start --source .

- Export ``FLYTECTL_CONFIG`` environment variable.

.. prompt:: bash $

  export FLYTECTL_CONFIG=$HOME/.flyte/config-sandbox.yaml

- Build Docker image

.. prompt:: base $

  flytectl sandbox exec -- docker build <code_directory> --tag "<code_directory>:v1"

- Package workflows

.. prompt:: bash $

  pyflyte --pkgs <code_directory> package --image <code_directory>:v1

- Register workflows

.. prompt:: bash $

  flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1
