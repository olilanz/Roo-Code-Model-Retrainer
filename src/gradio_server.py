import gradio as gr
from controller.controller import controller
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Controller instance: {controller}")
from controller.logger import setup_logger

# Stub functions for future integration
def get_workflow_state():
    """Stub function to retrieve the current workflow state."""
    return "Workflow state: Idle"

def get_logs():
    """Stub function to retrieve logs."""
    return "Logs:\n- Log entry 1\n- Log entry 2"

# Modular Gradio interface
# Set up logger
log_window_logs = []
def log_window_callback(log_entry):
    log_window_logs.append(log_entry)

logger = setup_logger(log_window_callback)

# Helpers for UI interactions
def download_model(model_link):
    logger.info(f"Download initiated for model: {model_link}")
    controller.add_log(f"Download initiated for model: {model_link}")
    return f"Downloading model: {model_link}"

# Create the Gradio interface layout
def create_interface():
    """Create the Gradio interface."""
    with gr.Blocks() as interface:
        # Title
        gr.Markdown("# Roo Code Model Retrainer")

        # Tabs
        with gr.Tabs():
            with gr.Tab("Models"):
                gr.Markdown("Manage your models here. You can download modeels from Huggingface for re-training.")

                gr.Markdown("### Add a Model")
                model_link = gr.Textbox(label="Model Link", placeholder="Enter Huggingface model link here")

                download_button = gr.Button("Download")
                download_result = gr.Textbox(label="Download Result", interactive=False)
                download_button.click(download_model, inputs=model_link, outputs=download_result)
                cancel_button = gr.Button("Cancel Download")

                gr.Markdown("### Downloaded Models")
                def fetch_models():
                    """Fetch models from the controller's in-memory state."""
                    return controller.models

                models_list = gr.Dataframe(
                    value=fetch_models(),
                    headers=["Name", "State", "Size (GB)", "Parameters", "Tensor Type"],
                    datatype=["str", "str", "number", "number", "str"],
                    interactive=False
                )
                
                refresh_button = gr.Button("Refresh Models")
                def refresh_models():
                    """Refresh the models list in the Gradio UI."""
                    return controller.models

                refresh_button.click(
                    lambda: controller.models,
                    outputs=models_list
                )

                delete_button = gr.Button("Delete Model")

            with gr.Tab("Testing"):
                gr.Markdown("Run tests against the models to evaluate their quality with regards to Roo Code interoperability.")
                gr.Markdown("[todo...]")

            with gr.Tab("Training"):
                gr.Markdown("Run the training process on a model.")
                gr.Markdown("[todo...]")

            with gr.Tab("Release"):
                gr.Markdown("Release a re-trained model to Huggiungface or Ollama.")
                gr.Markdown("[todo...]")

            with gr.Tab("Resources"):
                gr.Markdown("Monitor your system resources.")

                gr.Markdown("## Resources Dashboard")
                gr.Markdown("### GPU Monitoring")
                gr.Plot(label="GPU Memory Usage")
                gr.Plot(label="GPU Processing")
                gr.Plot(label="GPU Temperature")

        # Output
        with gr.Row():
            logs = gr.Textbox(label="Logs", value="\n".join(log_window_logs), interactive=False, elem_id="log-window")

    return interface

# Main function to launch the Gradio server
def main():
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()