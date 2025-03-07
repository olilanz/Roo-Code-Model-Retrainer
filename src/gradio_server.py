import gradio as gr
import logging
import controller.controller as controller
import asyncio

logger = logging.getLogger(__name__)

# Generic Task Scheduler that manages button locking and async task execution
async def task_scheduler(task_func, *inputs, button):
    # Lock the button (disable it) while the task is running
    button.update(interactive=False)

    try:
        # Execute the task function asynchronously
        result = await task_func(*inputs)
    except Exception as e:
        logger.error(f"Error during task execution: {e}")
        result = f"Error: {e}"

    # Once the task completes, unlock the button (enable it)
    button.update(interactive=True)
    return result

# Create the ui layout
def create_ui():
    """Create the Gradio user interface."""

    # Helpers for UI interactions
    def fetch_models():
        """Fetch the list of models and format them for the UI."""
        return [[model["name"], model["state"], model["size_gb"], model["parameters"], model["tensor_type"]] for model in controller.list_models()] 

    # Helper to download model using the task scheduler
    async def download_model_task(model_link):
        logger.info(f"Download initiated for model: {model_link}")
        controller.download_model(model_link)
        return None

    with gr.Blocks() as ui:
        # Title
        gr.Markdown("# Roo Code Model Retrainer")

        # Tabs
        with gr.Tabs():
            with gr.Tab("Models"):
                gr.Markdown("Manage your models here. You can download models from Huggingface for re-training.")

                gr.Markdown("### Add a Model")
                model_link = gr.Textbox(label="Model Link", placeholder="Enter Huggingface model link here")

                download_button = gr.Button("Download")

                # Pass the download_model_task function into the task_scheduler correctly
                download_button.click(
                    download_model_task,
                    inputs=[model_link],
                    outputs=[]
                )

                gr.Markdown("### Downloaded Models")
                models_list = gr.Dataframe(
                    value=fetch_models, 
                    headers=["Name", "State", "Size (GB)", "Parameters", "Tensor Type"],
                    datatype=["str", "str", "number", "number", "str"],
                    interactive=False
                )
                
            with gr.Tab("Testing"):
                gr.Markdown("Run tests against the models to evaluate their quality with regards to Roo Code interoperability.")
                gr.Markdown("[todo...]")

            with gr.Tab("Training"):
                gr.Markdown("Run the training process on a model.")
                gr.Markdown("[todo...]")

            with gr.Tab("Release"):
                gr.Markdown("Release a re-trained model to Huggingface or Ollama.")
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
            logs = gr.Textbox(label="Logs", value="Lalalalla", interactive=False, elem_id="log-window")

    return ui

# Main function to launch the Gradio server
def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
