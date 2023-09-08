import os 
import logging
from datetime import datetime

# get the directory of the current script
current_script_dir = os.path.dirname(
    os.path.abspath(__file__)
)

# Navigate up on directory and create a folder inside the root
project_dir = os.path.dirname(current_script_dir)
log_dir = os.path.join(project_dir, "Logs")
os.makedirs(log_dir, exist_ok=True)

# get the current dir and make the new file path for the app logs 

current_date = datetime.now().strftime("%Y-%m-%d")
logfile_path = os.path.join(
    log_dir,
    f"app_{current_date}.log"
)

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.FileHandler(logfile_path),  
        logging.StreamHandler(),  
    ]
)

# make a logger instance 
logger = logging.getLogger("covergpt_logger")