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

def download_model(name):
    """Simulate downloading a model with a delay."""
    if not name or name.strip() == "":
        raise ValueError("Model name is invalid: it cannot be empty or contain only whitespaces.")
    if any(model["name"] == name for model in _models):
        raise ValueError(f"Model '{name}' already exists in the list.")
    
    _logger.info(f"Downloading model {name}...")
    time.sleep(2)  # Simulate
    model = {
        "name": name,
        "state": "Downloaded",
        "size_gb": 1.0,  # Example size
        "parameters": 1000000000,  # Example parameters
        "tensor_type": "float32"
    }
    _models.append(model)
    _logger.info(f"Model {name} download completed.")

def remove_model(name):
    """Remove a model from the state."""
    global _models

    if not name or name.strip() == "":
        raise ValueError("Model name is invalid: it cannot be empty or contain only whitespaces.")
    if not any(model["name"] == name for model in _models):
        raise ValueError(f"Model '{name}' does not exist in the list.")
    
    _logger.info(f"Deleting model {name}...")
    time.sleep(2)  # Simulate
    _models = [model for model in _models if model["name"] != name]
    _logger.info(f"Model {name} deletion complete.")
