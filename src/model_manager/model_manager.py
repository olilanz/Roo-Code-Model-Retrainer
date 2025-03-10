import os
import shutil
import logging
from pathlib import Path
from transformers import AutoModel, AutoTokenizer, AutoConfig
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure HF_HOME is set
HF_HOME = os.environ.get("HF_HOME")
if not HF_HOME:
    raise EnvironmentError("HF_HOME environment variable is not set.")

def download_model(model_name: str) -> None:
    """
    Download a model from Hugging Face based on the model name.
    """
    try:
        logging.info(f"Starting download for model: {model_name}")
        model_path = Path(HF_HOME) / model_name
        AutoModel.from_pretrained(model_name, cache_dir=model_path)
        AutoTokenizer.from_pretrained(model_name, cache_dir=model_path)
        logging.info(f"Model '{model_name}' downloaded successfully to {model_path}")
    except Exception as e:
        logging.error(f"Failed to download model '{model_name}': {e}")
        raise

from transformers import AutoConfig

def list_models() -> list:
    """
    Enumerate all downloaded models in HF_HOME.
    Returns a list of dictionaries containing model names and metadata.
    """
    try:
        logging.info("Listing all downloaded models...")
        models = []
        hf_home_path = Path(HF_HOME)
        for model_dir in hf_home_path.iterdir():
            if model_dir.is_dir():
                fs_size_bytes = sum(f.stat().st_size for f in model_dir.glob("**/*") if f.is_file())
                fs_size = (
                    f"{fs_size_bytes / (1024 ** 3):.2f} GB" if fs_size_bytes >= 1024 ** 3 else
                    f"{fs_size_bytes / (1024 ** 2):.2f} MB" if fs_size_bytes >= 1024 ** 2 else
                    f"{fs_size_bytes / 1024:.2f} kB"
                )
                download_date = datetime.fromtimestamp(model_dir.stat().st_ctime).isoformat(timespec='seconds')

                metadata = {
                    "name": model_dir.name,
                    "folder_size": fs_size,
                    "download_date": download_date
                }

                try:
                    config_path = next(model_dir.glob("**/config.json"), None)
                    if config_path and config_path.exists():
                        config = AutoConfig.from_pretrained(config_path)
                    metadata.update({
                        "model_type": getattr(config, "model_type", "N/A"),
                        "model_architectures": getattr(config, "architectures", "N/A"),
                        "model_hidden_size": getattr(config, "hidden_size", "N/A"),
                        "model_trained_context_size": getattr(config, "max_position_embeddings", "N/A"),
                        "model_trained_parameters": getattr(config, "num_parameters", "N/A"),
                        "model_name_or_path": getattr(config, "_name_or_path", "N/A"),
                    })
                except Exception as e:
                    logging.warning(f"Failed to load config for {model_dir.name}: {e}")

                models.append(metadata)
        logging.info(f"Found {len(models)} models.")
        return models
    except Exception as e:
        logging.error(f"Failed to list models: {e}")
        raise

def delete_model(model_name: str) -> None:
    """
    Delete a downloaded model based on its name.
    """
    try:
        logging.info(f"Attempting to delete model: {model_name}")
        model_path = Path(HF_HOME) / model_name
        if model_path.exists() and model_path.is_dir():
            shutil.rmtree(model_path)
            logging.info(f"Model '{model_name}' deleted successfully.")
        else:
            logging.error(f"Model '{model_name}' not found in {HF_HOME}.")
            raise FileNotFoundError(f"Model '{model_name}' not found.")
    except Exception as e:
        logging.error(f"Failed to delete model '{model_name}': {e}")
        raise

def main():
    """
    CLI interface for the module.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Model Manager for Hugging Face models.")
    parser.add_argument("--download", type=str, help="Download a model by name.")
    parser.add_argument("--list", action="store_true", help="List all downloaded models.")
    parser.add_argument("--delete", type=str, help="Delete a model by name.")
    args = parser.parse_args()

    if args.download:
        download_model(args.download)
    elif args.list:
        models = list_models()
        for model in models:
            print(model)
    elif args.delete:
        delete_model(args.delete)
    else:
        print("No valid arguments provided. Use --help for usage information.")

if __name__ == "__main__":
    main()