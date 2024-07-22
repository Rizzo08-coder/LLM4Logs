# LLM4Logs

LLM4Logs tries to evaluate LLM performance with respect to log files analysis in the context of cybersecurity.
This guide will assist you in setting up the environment and configuring the necessary components.

The Colab notebooks used for the fine-tuning of the base Llama3 models are the following:
- [BETH](https://colab.research.google.com/drive/1Xu4gaapKSQc_Cva4vX23a-GfXfTUcOJq?usp=drive_link) - [huggingface](https://huggingface.co/Rizzo08/Llama3BETH)
- [UNSW](https://colab.research.google.com/drive/1r3cjKq6xGjmYzb-BaYPM0isj-EE5Ksi8?usp=drive_link) - [huggingface](https://huggingface.co/Rizzo08/Llama3UNSW)
- [ECML-PKDD](https://colab.research.google.com/drive/1x8Jt0EBkaOWMDhGtIOlnrzAPihW4BLxh?usp=drive_link) - [huggingface](https://huggingface.co/Rizzo08/Llama3ECMLPKDD)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Prerequisites

Ensure you have the following installed on your system:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

Clone the repository and start the Docker containers using the following commands:

```bash
git clone https://github.com/Rizzo08-coder/LLM4Logs
docker compose up
```

There are two containers:
- `llm4logs`: contains the Python interpreter and related dependencies
- `ollama`: based on the `ollama/ollama` image and includes on top of it the 3 finetuned LLM Models (llama3-beth, llama3-unsw, llama3-ecmlpkdd)

The images need to be built from the base provided by Docker.
Dependency installation and model building may take a while, and the resulting images may become quite large.

If you want to enable your Nvidia GPU for the inference process you can follow the official
[guidelines for the base `ollama/ollama` image](https://hub.docker.com/r/ollama/ollama) and update accordingly
the provided Docker Compose file.


## Usage

Python scripts for running inferences with generic LLMs are organized by dataset (inference_beth.py, inference_ecml_pkdd.py, inference_unsw.py), so the entry-point on llm4logs service in `docker-compose.yml` file needs to be modified based on the dataset you want to use.

Each of these scripts contains several hyperparameters to set:
- `model_name`: The name of the model to use for inferences, referring to the models available on Ollama.
- `number_of_shots`: The number of n-shots for the model with n >= 0.
- `useJson`: Boolean parameter that sets the response format of the LLM to JSON if `True`, otherwise the prompt instruct the LLM to return a number. This should be set `True` only for code-oriented models.

There is a separate script for fine-tuned LLMs (fine_tuning_inference.py), which also needs to be set as the entry-point. Based on the model used, the correct dataset will be automatically configured.

This script contains a single hyperparameter:
- `model_name`: The name of the fine-tuned model (`llama3-beth`, `llama3-unsw`, `llama3-ecmlpkdd`).

