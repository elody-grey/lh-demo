
##  Setup your environment 

### Install Littlehorse in your environment

Pip:
```shell
pip install typing_extensions=4.12.2
pip install littlehorse-client==0.11.2
```
Poetry:
```shell
poetry install
poetry shell
```

### Installing lhctl

```shell
brew install littlehorse-enterprises/lh/lhctl
```

### Installing Littlehorse server

```shell
docker run --name littlehorse -d -p 2023:2023 -p 8080:8080 ghcr.io/littlehorse-enterprises/littlehorse/lh-standalone:0.11.2
```

### Verify setup
```shell
lhctl version
```
It should print something similar to this:

``
lhctl version: 0.11.2 (Git SHA homebrew)
Server version: 0.11.2
``

### Python

```shell
poetry install
poetry shell
```

## Run

First lets initialize workers

```shell
python shopping.py
```

Then register the WfSpec

```shell
python workflow.py
```

