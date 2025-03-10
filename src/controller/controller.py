import logging
import time
import pandas as pd

import model_manager.model_manager as mm

_logger = logging.getLogger(__name__)

def list_models():
    """Return the models DataFrame with styling for row selection."""
    return pd.DataFrame(mm.list_models())

def download_model(name):
    """Simulate downloading a model with a delay."""
    global _models

    if not name.strip():
        _logger.error("Invalid model name: cannot be empty or whitespace.")
    else:
        mm.download_model(name)

    return list_models()  # Return styled DataFrame

def remove_model(name):
    """Remove a model from the list."""
    if not name.strip():
        _logger.error("Invalid model name: cannot be empty or whitespace.")
    else:
        mm.delete_model(name)

    return list_models()  # Return styled DataFrame
