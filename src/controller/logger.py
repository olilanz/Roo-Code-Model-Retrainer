import logging
from colorama import Fore, Style

class ColorFormatter(logging.Formatter):
    """Custom formatter to add color coding and timestamps to log messages."""
    def format(self, record):
        level_color = {
            "DEBUG": Fore.BLUE,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.MAGENTA
        }
        color = level_color.get(record.levelname, Fore.WHITE)
        reset = Style.RESET_ALL
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        message = f"{color}[{record.levelname}] {timestamp} - {record.getMessage()}{reset}"
        return message

def setup_logger(log_window_callback=None):
    """Set up the logger with color coding and optional Gradio log window integration."""
    logger = logging.getLogger("controller_logger")
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColorFormatter())
    console_handler.formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Gradio log window handler
    if log_window_callback:
        class GradioHandler(logging.Handler):
            def emit(self, record):
                log_entry = self.format(record)
                log_window_callback(log_entry)

        gradio_handler = GradioHandler()
        gradio_handler.setLevel(logging.DEBUG)
        gradio_handler.setFormatter(ColorFormatter())
        gradio_handler.formatter.datefmt = "%Y-%m-%d %H:%M:%S"
        logger.addHandler(gradio_handler)

    return logger