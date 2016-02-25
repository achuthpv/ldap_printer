import os


def get_project_root():
    project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return project_root
