import os
import yaml

def load_config(config_path: str = None) -> dict:
    # Always resolve path relative to /app (works in Docker and locally)
    base_dir = os.path.dirname(os.path.dirname(__file__))  # -> /app
    default_path = os.path.join(base_dir, "config", "config.yaml")

    path = config_path or default_path

    with open(path, "r") as file:
        return yaml.safe_load(file)
