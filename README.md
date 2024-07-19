# Advanced LLM Inference Environment

Welcome to the repository for advanced Large Language Model (LLM) inference. This guide will assist you in setting up the environment and configuring the necessary components.

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

There will be created two containers:
- `llm4logs` -> contains the python interpreter and dependencies 
- `ollama` -> contains ollama image and the 3 finetuned LLM Models (llama3-beth, llama3-unsw, llama3-ecmlpkdd)


## Usage

Python scripts for running inferences with generic LLMs are organized by dataset (inference_beth.py, inference_ecml_pkdd.py, inference_unsw.py), so the entry-point in the `docker-compose.yml` file needs to be modified based on the dataset you want to use.

Each of these scripts contains several hyperparameters to set:
- `model_name`: The name of the model to use for inferences, referring to the models available on Ollama.
- `number_of_shots`: The number of n-shots for the model with n >= 0.
- `useJson`: Boolean parameter that sets the response format of the LLM to JSON if `True`, otherwise a number. This should be set to `True` for code-oriented models.

There is a separate script for fine-tuned LLMs (fine_tuning_inference.py), which also needs to be set as the entry-point. Based on the model used, the correct dataset will be automatically configured.

This script contains a single hyperparameter:
- `model_name`: The name of the fine-tuned model (`llama3-beth`, `llama3-unsw`, `llama3-ecmlpkdd`).

