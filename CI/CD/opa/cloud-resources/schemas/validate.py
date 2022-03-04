#!/usr/bin/env python3
"""  Simple Cerberus Validator Script testing1010"""
from cerberus import Validator #pylint: disable=import-error
import yaml #pylint: disable=import-error
with open('../../cloud-resources/processed_params.yml') as f:
    DATA = yaml.load(f, Loader=yaml.FullLoader)

with open('gcp_project_schemas/big-query-dataset_schema.yml') as f:
    SCHEMA = yaml.load(f, Loader=yaml.FullLoader)

V = Validator()
V.allow_unknown = True

if V.validate(DATA, SCHEMA):
    print('Pass')
else:
    print('Fail')
    ERR = V.errors
    print(ERR)
