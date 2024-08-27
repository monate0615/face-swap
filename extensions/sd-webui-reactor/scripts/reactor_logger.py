import logging
import copy
import sys

from modules import shared
from scripts.reactor_globals import IS_RUN
from scripts.reactor_helpers import addLoggingLevel


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;36m",  # CYAN
        "STATUS": "\033[38;5;173m",  # Calm ORANGE
        "INFO": "\033[0;32m",  # GREEN
        "WARNING": "\033[0;33m",  # YELLOW
        "ERROR": "\033[0;31m",  # RED
        "CRITICAL": "\033[0;37;41m",  # WHITE ON RED
        "RESET": "\033[0m",  # RESET COLOR
    }

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = self.COLORS.get(levelname, self.COLORS["RESET"])
        colored_record.levelname = f"{seq}{levelname}{self.COLORS['RESET']}"
        return super().format(colored_record)


# Create a new logger
logger = logging.getLogger("ReActor")
logger.propagate = False

# Add Custom Level
addLoggingLevel("STATUS", logging.INFO + 5)

# Add handler if we don't have one.
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s","%H:%M:%S")
    )
    logger.addHandler(handler)

# Configure logger
loglevel_string = getattr(shared.cmd_opts, "reactor_loglevel", "INFO")
loglevel = getattr(logging, loglevel_string.upper(), "info")
logger.setLevel(loglevel)

def set_Run(value):
    global IS_RUN
    IS_RUN = value

def get_Run():
    global IS_RUN
    return IS_RUN
