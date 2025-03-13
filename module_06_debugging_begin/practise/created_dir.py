import os
import re


def creted_dir_for_logs(current_path, module) -> str:
    """
    Function for created the directory
    """
    os.chdir(current_path)
    current_file = module.split(re.findall(r"[\\\\/]", __file__)[0])[-1].split('.')[0]
    dir_path = os.path.join("logs", f'{current_file}')

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    
    return dir_path
