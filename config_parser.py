from ruamel.yaml import YAML
import os

yaml = YAML()
CONF_FILE_PATH = os.path.join("config-env.yml")
conf_fp = open(CONF_FILE_PATH, "r")
env = yaml.load(conf_fp)

