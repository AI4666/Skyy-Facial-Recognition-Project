import json
from pathlib import Path

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the path to the config file - read from @config.json\config.json
CONFIG_FILE = BASE_DIR / "config.json" / "config.json"

def load_config() -> dict:
    """Loads the configuration from @config.json/config.json"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {CONFIG_FILE}")
    
    # Resolve relative paths to absolute paths
    config['database']['persist_directory'] = str(BASE_DIR / config['database']['persist_directory'])
    config['storage']['image_storage_path'] = str(BASE_DIR / config['storage']['image_storage_path'])
    config['logging']['log_file'] = str(BASE_DIR / config['logging']['log_file'])
    
    return config

# Load the config to be imported by other modules
config = load_config()

# Ensure necessary directories exist - handle both file and directory conflicts
def ensure_dir(path_str):
    path = Path(path_str)
    if path.exists() and path.is_file():
        path.unlink()  # Remove file if it exists
    path.mkdir(parents=True, exist_ok=True)

ensure_dir(config['database']['persist_directory'])
ensure_dir(config['storage']['image_storage_path'])
ensure_dir(Path(config['logging']['log_file']).parent)