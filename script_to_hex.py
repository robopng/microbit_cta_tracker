import shutil
import subprocess
import os


def convert(path):
    """
    Convert a provided micropython file to .hex code, and send it
    to the connected micro:bit device.
    :param path: path to the micropython file
    """
    # subprocess.run(['uflash', path])
    assert os.path.isfile(path)
    subprocess.run(['py2hex', path])
    push(os.path.join(path, r'..\__temp_dynamic_out.hex'))


def push(path):
    """
    Push a .hex code file to the connected micro:bit device for flashing.
    :param path: path to the .hex code file
    """
    path = os.path.join(os.getcwd(), path)
    shutil.copyfile(path, "D:/script.hex")
