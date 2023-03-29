# sshlab

Jupyter notebook / lab through ssh with a single command and config file

This script is inspired by https://github.com/nicolaschotard/stackyter but reimplemented to allow starting Jupyter in a container (singularity or docker) in the remote server

# Usage

Copy the example settings file `.sshlab_config.yml` to your HOME and edit it to your needs.

## Install

```
pip install .
```

## Run 

```
sshlab -c singularity_config
```

