#pylint: disable=R1732
#!/usr/bin/env python3
'''
Jinja tempale rendering and final yaml validation after it
'''

import os
import sys
import glob
import subprocess
import yaml #pylint: disable=import-error
from jinja2 import Environment, FileSystemLoader #pylint: disable=import-error
from yamllint.config import YamlLintConfig #pylint: disable=import-error
from yamllint import linter #pylint: disable=import-error


VAR_DIR = 'test_vars/gcp_project/'
TEMPL_DIR = 'templates/gcp-project/'
CONF = YamlLintConfig('extends: default')

for dirname in os.listdir(VAR_DIR):
    if os.path.isdir(os.path.join(VAR_DIR, dirname)):
        subprocess.call(['yq merge --allow-empty ' + VAR_DIR + dirname + '/*.yml > ' +
                         VAR_DIR + dirname + '.yml'], shell=True)
        for filename in glob.glob(TEMPL_DIR + '*.yml.j2'):
            config = yaml.load(open(VAR_DIR + dirname + '.yml'))
            env = Environment(loader=FileSystemLoader('./'), lstrip_blocks=True)
            template = env.get_template(filename)
            print("--> Processing project " + dirname + " with rendering template: " + filename)
            output = template.render(config)
            gen = linter.run(output, CONF)
            errors = list(gen)
            for i in errors:
                print(i)
                if 'syntax error:' in str(i):
                    sys.exit(">>> Syntax check failed")
