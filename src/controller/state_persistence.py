import json
import os

def save_state(state, file_path):
    """Save the state to a file."""
    with open(file_path, "w") as f:
        json.dump(state, f)

def load_state(file_path):
    """Load the state from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}