import os

def get_registry_root():
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/../registry')

