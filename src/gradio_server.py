import gradio as gr
import logging
import controller.controller as controller

# Storing logs in a buffer 
MAX_LOGS = 50
logs_buffer = []

def get_logs():
    return "\n".join(logs_buffer)

# Create the UI layout
def create_ui():
    """Create the Gradio user interface."""
    
    def models_tab():
        with gr.Tab("Models"):
            gr.Markdown("### Downloaded Models")
            models_grid = gr.Dataframe(
                value=controller.list_models(),  # Populate here before launch
                interactive=False
            )
            gr.Markdown("Manage your models here. You can download models from Huggingface for re-training. Provide the name of the model (e.g. Qwen/QwQ-32B) and press teh download button. You can also remove models by providing the model name and pressing the delete button.")
            with gr.Accordion("Download or remove models", open=False):
                model_name = gr.Textbox(placeholder="Enter Huggingface model name", show_label=False)
                with gr.Row():
                    download_button = gr.Button("Download")
                    download_button.click(
                        controller.download_model,
                        inputs=[model_name], outputs=[models_grid]
                    ) 
                    delete_button = gr.Button("Delete")
                    delete_button.click(
                        controller.remove_model,
                        inputs=[model_name], outputs=[models_grid],
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
            logs = gr.Code(
                label="Logs", 
                language="shell", 
                every=1, 
                max_lines=MAX_LOGS, 
                value=get_logs, 
                interactive=False)
    return ui

def setup_log_handler():
    # log handler to be registered with root logger
    class GradioLogHandler(logging.Handler):
        def __init__(self, output_fn):
            super().__init__()
            self.output_fn = output_fn
    
        def emit(self, record):
            log_message = self.format(record)
            self.output_fn(log_message)

    # helper that stores all log messages in buffer
    def update_logs(log_message):
        global logs_buffer
        logs_buffer.append(log_message)  # Append new log message to the list
        logs_buffer = logs_buffer[-MAX_LOGS:]  # Keep the last 100 log messages
        
    # Attach the log handler to the root logger
    logging.getLogger().addHandler(GradioLogHandler(output_fn=update_logs))

def main():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    setup_log_handler()

    ui = create_ui()
    ui.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
