import os
import shutil
import logging
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

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
                metadata = {
                    "name": model_dir.name,
                    "path": str(model_dir),
                    "size": sum(f.stat().st_size for f in model_dir.glob("**/*") if f.is_file()),
                    "creation_date": model_dir.stat().st_ctime
                }
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