AWS Sagemaker distributed training using PyTorch
--------------------------------------------------

Creating a dockerfile for Sagemaker custom training [Required]
===============================================================

.. literalinclude:: ../../smpytorch.Dockerfile
    :language: dockerfile
    :emphasize-lines: 1, 22-24
    :linenos:
    :caption: Dockerfile for Sagemaker, similar to base dockerfile, but installs sagemaker-training and sets training script
