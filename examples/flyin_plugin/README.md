(flyte-interactive)=

# FlyIn Plugin

```{eval-rst}
.. tags:: Advanced
```

Flyte tasks, designed as one-off jobs, require users to wait until completion to view results. These tasks are developed locally in a virtual environment before being deployed remotely. However, differences in data access, GPU availability, and dependencies between local and remote environments often lead to discrepancies, making local success an unreliable indicator of remote success. This results in frequent, tedious debugging cycles.


To address this, "FlyIn" has been introduced. It serves as a bridge between local and remote development, providing a feature-riched IDE on the browser. This allows developers to leverage remote environment capabilities while accessing features like debugging, code inspection, and Jupyter Notebook, traditionally available in local IDEs.


## Installation

To use the flyte interactive plugin simply run the following:

```{eval-rst}
.. prompt:: bash

    pip install flytekitplugins-flyin
```


## Acknowledgement

This feature was created at LinkedIn and later donated to Flyte.

```{auto-examples-toc}
vscode.py
```