import json
import os

class Controller:
    """Singleton Controller class to manage global state."""
    _instance = None
    _state_file = "controller_state.json"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls, *args, **kwargs)
            cls._instance.models = [
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
            cls._instance.logs = []
            cls._instance._load_state()
        return cls._instance

    def _load_state(self):
        """Load the state from a file."""
        if os.path.exists(self._state_file):
            with open(self._state_file, "r") as f:
                state = json.load(f)
                self.models = state.get("models", [])
                self.logs = state.get("logs", [])

    def _save_state(self):
        """Save the state to a file."""
        state = {
            "models": self.models,
            "logs": self.logs
        }
        with open(self._state_file, "w") as f:
            json.dump(state, f)

    def download_model(self, model_name):
        """Simulate downloading a model with a delay."""
        import time
        time.sleep(5)  # Simulate a 5-second download delay
        model = {
            "name": model_name,
            "state": "Downloaded",
            "size_gb": 1.0,  # Example size
            "parameters": 1000000000,  # Example parameters
            "tensor_type": "float32"
        }
        self.models.append(model)
        self._save_state()

    def remove_model(self, name):
        """Remove a model from the state."""
        self.models = [model for model in self.models if model["name"] != name]
        self._save_state()
        return cls._instance

    # Removed redundant add_model function

    # Removed duplicate remove_model and download_model methods
    def update_model_state(self, name, state):
        """Update the state of a model."""
        for model in self.models:
            if model["name"] == name:
                model["state"] = state
                break
        self._save_state()

    def download_model(self, model_name):
        """Simulate downloading a model with a delay."""
        import time
        time.sleep(5)  # Simulate a 5-second download delay
        log_entry = f"Model {model_name} downloaded successfully."
        self.logs.append(log_entry)
        self._save_state()

    def add_log(self, log_entry):
        """Add a log entry."""
        self.logs.append(log_entry)
        self._save_state()

    def get_logs(self):
        """Retrieve logs."""
        return self.logs

    def _save_state(self):
        """Save the state to a file."""
        state = {
            "models": self.models,
            "logs": self.logs
        }
        with open(self._state_file, "w") as f:
            json.dump(state, f)

    def _load_state(self):
        """Load the state from a file."""
        if os.path.exists(self._state_file):
            with open(self._state_file, "r") as f:
                state = json.load(f)
                self.models = state.get("models", [])
                self.logs = state.get("logs", [])

# Singleton instance
controller = Controller()