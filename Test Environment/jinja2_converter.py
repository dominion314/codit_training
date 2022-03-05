import json
import pyaml
import jinja2
from jinja2 import Environment, PackageLoader, FileSystemLoader
import sys

##Open JSON file and save it as dump_data
with open('doms-merch-xpn-lle.json', 'r') as f:
    data = json.load(f)
    dump_data = json.dumps(data, sort_keys=True)

#Create list of all info from dump_data to the output1.yml.
list = pyaml.dump(dump_data, safe=True)
#print(list)

#Have Jinja take the list data and render it to the template.j2 structure

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('/Users/tkma4f8/JSONtoYAML')) 
template = jinja_env.get_template('template.j2')
print(template.render(list))