import sys
import ruamel.yaml

yaml = ruamel.yaml.YAML()
# yaml.preserve_quotes = True
with open("input.yaml") as fp:
    data = yaml.load(fp)
for elem in data:
    if elem["name"] == "sense2":
        elem["value"] = 1234
        break  # no need to iterate further
yaml.dump(data, sys.stdout)
