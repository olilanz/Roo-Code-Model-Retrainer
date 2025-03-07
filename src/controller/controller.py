import json
import os

class Controller:
    """Singleton Controller class to manage global state."""
    _instance = None
    _state_file = "controller_state.json"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls, *args, **kwargs)
            cls._instance.models = []
            cls._instance.logs = []
            cls._instance._load_state()
        return cls._instance

    def add_model(self, name, state, size_gb, parameters, tensor_type):
        """Add a model to the state."""
        model = {
            "name": name,
            "state": state,
            "size_gb": size_gb,
            "parameters": parameters,
            "tensor_type": tensor_type
        }
        self.models.append(model)
        self._save_state()

    def remove_model(self, name):
        """Remove a model from the state."""
        self.models = [model for model in self.models if model["name"] != name]
        self._save_state()

    def update_model_state(self, name, state):
        """Update the state of a model."""
        for model in self.models:
            if model["name"] == name:
                model["state"] = state
                break
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