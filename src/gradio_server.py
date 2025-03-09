import gradio as gr
import logging
import controller.controller as controller
import asyncio

logger = logging.getLogger(__name__)

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
                        controller.download_model,
                        inputs=[model_name], outputs=[]
                    )
                    delete_button = gr.Button("Delete")
                    delete_button.click(
                        controller.remove_model,
                        inputs=[model_name], outputs=[]
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

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
