from typing import Dict, Any
import yaml

def unyaml_thing(file_path: str = 'thing.yml') -> Dict[str, Any]:
    """ Extract a python object from a yaml file and return it

    Args:
        file_path: the file, optionally along with a path to another directory
        (default: {'thing.yml'})

    Returns:
        the yaml as a nested dictionary
    """
    with open(file_path, 'r') as f:
        thing = yaml.safe_load(f)
    return thing
