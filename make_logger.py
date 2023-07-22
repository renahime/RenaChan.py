import logging
import colorlog

def initialize_logger():
    # Create a logger object
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.INFO)

    # Create a formatter that includes color information
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
        log_colors={
            'DEBUG': 'white',
            'INFO': 'purple',      # Use purple for INFO messages
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        reset=True
    )

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    # Optionally, you can return the logger if you need to use it in the main script
    return logger
