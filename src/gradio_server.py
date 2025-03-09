import gradio as gr
import logging
import controller.controller as controller

logger = logging.getLogger(__name__)

logs_buffer = ["lkjlkj", "lkjlkj", "lkjlkj"]

def get_logs():
    return "\n".join(logs_buffer)

# Create the UI layout
def create_ui():
    """Create the Gradio user interface."""
    def fetch_models():
        """Fetch the list of models and format them for the UI."""
        return [[model["name"], model["state"], model["size_gb"], model["parameters"], model["tensor_type"]]
                for model in controller.list_models()]

    def models_tab():
        with gr.Tab("Models"):
            gr.Markdown("Manage your models here. You can download models from Huggingface for re-training.")
            gr.Markdown("### Downloaded Models")
            models_list = gr.Dataframe(
                value=fetch_models,
                headers=["Name", "State", "Size (GB)", "Parameters", "Tensor Type"],
                datatype=["str", "str", "number", "number", "str"],
                interactive=False
            )
            with gr.Accordion("Download or remove models", open=False):
                model_name = gr.Textbox(placeholder="Enter Huggingface model name", show_label=False)
                with gr.Row():
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

    def testing_tab():
        with gr.Tab("Testing"):
            gr.Markdown("Run tests against the models...")
            gr.Markdown("[todo...]")

    def training_tab():
        with gr.Tab("Training"):
            gr.Markdown("Run the training process on a model.")
            gr.Markdown("[todo...]")

    def release_tab():
        with gr.Tab("Release"):
            gr.Markdown("Release a re-trained model...")
            gr.Markdown("[todo...]")

    def resources_tab():
        with gr.Tab("Resources"):
            gr.Markdown("Monitor your system resources.")
            gr.Markdown("## Resources Dashboard")
            gr.Markdown("### GPU Monitoring")
            gr.Plot(label="GPU Memory Usage")
            gr.Plot(label="GPU Processing")
            gr.Plot(label="GPU Temperature")

    with gr.Blocks() as ui:
        gr.Markdown("# Roo Code Model Retrainer")
        with gr.Tabs():
            models_tab()
            testing_tab()
            training_tab()
            release_tab()
            resources_tab()
        with gr.Row():
            logs = gr.Code(label="Logs", language="shell", every=1, value=get_logs, interactive=False, elem_id="log-window")
    return ui

def main():

    class GradioLogHandler(logging.Handler):
        def __init__(self, output_fn):
            super().__init__()
            self.output_fn = output_fn
        
        def emit(self, record):
            log_message = self.format(record)
            self.output_fn(log_message)

    def update_logs(log_message):
        logs_buffer.append(log_message)  # Append new log message to the list
        logs_buffer = logs_buffer[-100:]  # Keep the last 100 log messages
        print("Logs buffer updated:", logs_buffer)
    
    # Debugging logger configuration
    print("Logger level:", logger.level)
    print("Handlers attached to logger:", logger.handlers)


    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger.addHandler(GradioLogHandler(output_fn=update_logs))

    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
