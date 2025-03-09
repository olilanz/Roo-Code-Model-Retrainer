import logging
import time
import pandas as pd

_logger = logging.getLogger(__name__)

_models = pd.DataFrame([
    {"name": "GPT-4", "state": "Available", "size_gb": 1.2, "parameters": 175e9, "tensor_type": "float32"},
    {"name": "BERT", "state": "Available", "size_gb": 0.4, "parameters": 110e6, "tensor_type": "float32"},
    {"name": "LLaMA", "state": "Available", "size_gb": 2.0, "parameters": 65e9, "tensor_type": "float32"}
])

def list_models():
    """Return the models DataFrame with styling for row selection."""
    return _models.style.set_properties(**{
        'cursor': 'pointer',  # Makes the entire row clickable
        'user-select': 'none'  # Prevents individual cell selection
    }).set_table_styles([
        {'selector': 'tr:hover', 'props': [('background-color', '#d3d3d3')]}  # Highlights full row on hover
    ])

def download_model(name):
    """Simulate downloading a model with a delay."""
    global _models

    if not name.strip():
        _logger.error("Invalid model name: cannot be empty or whitespace.")
    elif name in _models["name"].values:
        _logger.error(f"Model '{name}' already exists.")
    else:
        _logger.info(f"Downloading model {name}...")
        time.sleep(2)  # Simulate
        _models = pd.concat([_models, pd.DataFrame([{
            "name": name, "state": "Downloaded", "size_gb": 1.0,
            "parameters": 1e9, "tensor_type": "float32"
        }])], ignore_index=True)
        _logger.info(f"Model {name} download completed.")

    return list_models()  # Return styled DataFrame

def remove_model(name):
    """Remove a model from the list."""
    global _models

    if not name.strip():
        _logger.error("Invalid model name: cannot be empty or whitespace.")
    elif name not in _models["name"].values:
        _logger.error(f"Model '{name}' not found.")
    else:
        _logger.info(f"Deleting model {name}...")
        time.sleep(2)  # Simulate
        _models = _models[_models["name"] != name]
        _logger.info(f"Model {name} deleted.")

    return list_models()  # Return styled DataFrame
