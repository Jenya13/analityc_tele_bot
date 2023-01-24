import os
from pathlib import Path
from os.path import join, dirname
from dotenv import load_dotenv


def get_from_env(key):
    env_path = Path(dirname(__file__)).parents[0]
    dotenv_path = join(env_path, '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)
