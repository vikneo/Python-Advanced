import os
import shlex
import subprocess

BASE_DIR = os.path.dirname(__file__)
homework_db = os.path.join(BASE_DIR, "homework.db")


def create_db():
    cmd = "python -m module_19_db4.generate_practice_and_homework_db"
    cmd_list = shlex.split(cmd)
    subprocess.Popen(cmd_list, stdout=subprocess.PIPE, close_fds=False)


if __name__ == "__main__":
    create_db()
