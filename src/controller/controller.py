import logging
import time

_logger = logging.getLogger(__name__)

_models = [
    {
        "name": "GPT-4",
        "state": "Available",
        "size_gb": 1.2,
        "parameters": 175000000000,
        "tensor_type": "float32"
    },
    {
        "name": "BERT",
        "state": "Available",
        "size_gb": 0.4,
        "parameters": 110000000,
        "tensor_type": "float32"
    },
    {
        "name": "LLaMA",
        "state": "Available",
        "size_gb": 2.0,
        "parameters": 65000000000,
        "tensor_type": "float32"
    }
]

def list_models():
    """Return a list of models."""
    return _models

def download_model(model_name):
    """Simulate downloading a model with a delay."""
    time.sleep(5)  # Simulate a 5-second download delay
    model = {
        "name": model_name,
        "state": "Downloaded",
        "size_gb": 1.0,  # Example size
        "parameters": 1000000000,  # Example parameters
        "tensor_type": "float32"
    }
    _models.append(model)
    _logger.info(f"Model {model_name} downloaded successfully.")

def remove_model(name):
    """Remove a model from the state."""
    global _models
    _models = [model for model in _models if model["name"] != name]

def update_model_state(name, state):
    """Update the state of a model."""
    for model in _models:
        if model["name"] == name:
            model["state"] = state
            break
