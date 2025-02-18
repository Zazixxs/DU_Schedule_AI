Here is a more organized version of the installation instructions:

# Installation Guide

## Prerequisites

### Install Ollama
Visit [Ollama's website](https://ollama.com/) to download and install.

### Install Docker Desktop
Visit [Docker Desktop](https://www.docker.com/products/docker-desktop/) to download and install.

### Install Python Dependencies
```sh
pip install flask
pip install BeautifulSoup
```

## Docker Setup

### Pull Ollama Docker Image
```sh
docker pull ollama/ollama
```

## Choose Models in Ollama

Pull selected models from [Ollama Search](https://ollama.com/search).

## Manual Setup

### Start Ollama in Command Prompt
```sh
ollama serve
```

### Run the Flask Application
Navigate to your Flask application directory and run:
```sh
python localpath/Flask/app.py
```

### Default Ports
- **Flask**: Runs on `localhost:3000`
- **Ollama**: Runs on `localhost:11434`

You can update the README.md with these changes.
