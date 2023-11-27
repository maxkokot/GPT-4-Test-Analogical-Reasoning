import yaml


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return config


def load_txt(path):
    with open(path, 'r') as f:
        file = f.read()
    return file
