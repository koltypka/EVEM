import yaml
from yaml.loader import SafeLoader

def getYamlFile(filePath):
    with open(filePath) as f:
        parametrs = yaml.load(f, Loader=SafeLoader)
    return parametrs