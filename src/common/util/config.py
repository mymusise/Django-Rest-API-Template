import os
import pathlib

from dotenv import load_dotenv


def load_config():
    dot_file_path = "/configs/.env"
    if os.path.exists(dot_file_path):
        load_dotenv(dot_file_path)
    else:
        env_path = os.path.join(
            pathlib.Path(__file__).parent.parent.parent.absolute(), "./server/.env"
        )
        load_dotenv(env_path)
