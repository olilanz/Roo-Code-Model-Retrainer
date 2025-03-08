import gradio as gr
import logging
import controller.controller as controller
import asyncio

logger = logging.getLogger(__name__)
MAIN_LOOP = None  # Global variable to store the main event loop

def run_task(task_func, *inputs, button=None):
    async def _task_runner(task_func, *inputs, button=None):
        # Lock button and show loading state
        if button:
            button.update(interactive=False, value="Processing...", variant="primary")
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, task_func, *inputs)
        except Exception as e:
            logger.error(f"Error during task execution: {e}")
            result = f"Error: {e}"
        if button:
            button.update(interactive=True, value="Done!", variant="success")
            await asyncio.sleep(1)
            button.update(value="Done", variant="primary")
        return result

    # Schedule the coroutine on the main loop
    asyncio.run_coroutine_threadsafe(_task_runner(task_func, *inputs, button=button), MAIN_LOOP)
    # Explicitly return None so no output is passed back to Gradio.
    return None


# Create the UI layout
def create_ui():
    """Create the Gradio user interface."""
    def fetch_models():
        """Fetch the list of models and format them for the UI."""
        return [[model["name"], model["state"], model["size_gb"], model["parameters"], model["tensor_type"]] 
                for model in controller.list_models()]

    with gr.Blocks() as ui:
        gr.Markdown("# Roo Code Model Retrainer")

        with gr.Tabs():
            with gr.Tab("Models"):
                gr.Markdown("Manage your models here. You can download models from Huggingface for re-training.")
                gr.Markdown("### Downloaded Models")
                models_list = gr.Dataframe(
                    value=fetch_models,
                    headers=["Name", "State", "Size (GB)", "Parameters", "Tensor Type"],
                    datatype=["str", "str", "number", "number", "str"],
                    interactive=False
                )
                gr.Markdown("### Add/remove a Model")
                with gr.Row():
                    model_name = gr.Textbox(placeholder="Enter Huggingface model name", show_label=False)
                    download_button = gr.Button("Download")
                    download_button.click(
                        fn=lambda: run_task(controller.download_model, model_name, button=download_button),
                        inputs=[], outputs=[]
                    )
                    delete_button = gr.Button("Delete")
                    delete_button.click(
                        fn=lambda: run_task(controller.remove_model, model_name, button=delete_button),
                        inputs=[], outputs=[]
                    )
            with gr.Tab("Testing"):
                gr.Markdown("Run tests against the models...")
                gr.Markdown("[todo...]")
            with gr.Tab("Training"):
                gr.Markdown("Run the training process on a model.")
                gr.Markdown("[todo...]")
            with gr.Tab("Release"):
                gr.Markdown("Release a re-trained model...")
                gr.Markdown("[todo...]")
            with gr.Tab("Resources"):
                gr.Markdown("Monitor your system resources.")
                gr.Markdown("## Resources Dashboard")
                gr.Markdown("### GPU Monitoring")
                gr.Plot(label="GPU Memory Usage")
                gr.Plot(label="GPU Processing")
                gr.Plot(label="GPU Temperature")
        with gr.Row():
            logs = gr.Textbox(label="Logs", value="Lalalalla", interactive=False, elem_id="log-window")
    return ui

def main():
    global MAIN_LOOP
    # Create a new event loop and set it as the global MAIN_LOOP.
    MAIN_LOOP = asyncio.new_event_loop()
    asyncio.set_event_loop(MAIN_LOOP)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
