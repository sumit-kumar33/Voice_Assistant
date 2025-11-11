import logging
from config_files.config import Name

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    filename=f"{Name}.log",
    format='%(asctime)s %(levelname)s: %(message)s'
    )

messages: logging.Logger = logging.getLogger(__name__)

handler = logging.FileHandler(f"{Name} messages.log")
formatter = logging.Formatter("%(asctime)s: %(message)s")
console_handler = logging.StreamHandler()

handler.setFormatter(formatter)
messages.addHandler(handler)
messages.addHandler(console_handler)

def startup_log() -> None:
    logging.info("=" * 50 + f"{Name} is starting" + "=" * 50)
    messages.info("=" * 50 + f"{Name} is starting" + "=" * 50)