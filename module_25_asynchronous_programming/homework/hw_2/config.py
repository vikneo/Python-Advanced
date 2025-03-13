from pathlib import Path
from datetime import datetime


URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent
OUT_PATH_DIR = OUT_PATH / 'cats'
OUT_PATH_DIR.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()
TIME_OUT = 15


