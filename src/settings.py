import yaml

with open('config.yml', 'r', encoding='utf-8') as f:
    _config = yaml.safe_load(f)
with open('secrets.yml', 'r', encoding='utf-8') as f:
    _secrets = yaml.safe_load(f)

PREFIXES = _config['prefixes']
TOKEN = _secrets['token']
