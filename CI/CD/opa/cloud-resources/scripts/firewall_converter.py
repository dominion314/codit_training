#pylint: disable=W0611,E1120,W0612,C0116,W0622,W0612,C0121,C0103,R1710,W0613,C0115,R1725,E0401,C0114,C0304,W0311,C0303,C0325,R0903
from os import closerange
from typing import ValuesView
import sys
import logging
import json
import yaml
import click

class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

class QuotedString(str):
    pass

def quoted_scalar(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

@click.command()
@click.argument('filename')
@click.pass_obj
def main(ctx_obj, filename):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./integrity_check.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)
    project_input = readFile(filename)
    normalize(project_input)

def str2bool(v):
    return str(v).lower() in ("true")
     
def parse_allowed_values(allowed):
    if allowed == "":
        return
    list_data = allowed.split(",")
    new_data = []
    for item in list_data:
        data = item.strip().replace("'", "").replace("[", "").replace("]", "")
        new_data.append(data)
    values = []
    tcp_ports = {"protocol": QuotedString("tcp"), "ports": []}
    udp_ports = {"protocol": QuotedString("udp"), "ports": []}
    icmp = {"protocol": "icmp"}
    for item in new_data:
        if item == "icmp":
            values.append(icmp)
        if ":" in item:
            data = item.split(":")
            protocol = data[0]
            port = data[1]
            if protocol == "tcp":
                tcp_ports["ports"].append(QuotedString(port))
            elif protocol == "udp":
                udp_ports["ports"].append(QuotedString(port))
    if tcp_ports["ports"] != []:
        values.append(tcp_ports)
    if udp_ports["ports"] != []:
        values.append(udp_ports)
    return values

def parse_denied_values(denied):
    if denied == "":
        return
    list_data = denied.split(",")
    new_data = []
    for item in list_data:
        data = item.strip().replace("'", "").replace("[", "").replace("]", "")
        new_data.append(data)
    values = []
    tcp_ports = {"protocol": QuotedString("tcp"), "ports": []}
    udp_ports = {"protocol": QuotedString("udp"), "ports": []}
    icmp = {"protocol": "icmp"}
    for item in new_data:
        if item == "icmp":
            values.append(icmp)
        if ":" in item:
            data = item.split(":")
            protocol = data[0]
            port = data[1]
            if protocol == "tcp":
                tcp_ports["ports"].append(QuotedString(port))
            elif protocol == "udp":
                udp_ports["ports"].append(QuotedString(port))
    if tcp_ports["ports"] != []:
        values.append(tcp_ports)
    if udp_ports["ports"] != []:
        values.append(udp_ports)
    return values

def readFile(inFile) -> list:
    MyDumper.add_representer(QuotedString, quoted_scalar)
    try:
        with open(inFile, 'r') as file:
            return (json.load(file))
    except FileNotFoundError:
        logging.error("Error with input file: Not Found!")
        sys.exit(1)

def cleanNullTerms(d):
   clean = {}
   for item in list(d.keys()):
       for sum in list(d[item].keys()):
        if sum == "rule":
            for key in list(d[item]["rule"].keys()):
                if d[item]["rule"].get(key) == None:
                    d[item]["rule"].pop(key)
        elif d[item].get(sum) == None:
                d[item].pop(sum)

def normalize(input) -> list:
    MyDumper.add_representer(QuotedString, quoted_scalar)
    output = []
    for item in input:
        if "dflt" in item["name"]:
            continue
        allowed_data = parse_allowed_values(item["allowed"])
        denied_data = parse_allowed_values(item["denied"])
        if item["targetTags"] == "":
            target_tags = None
        else:
            target_tags = item["targetTags"].split(",")
        if item["sourceTags"] == "":
            source_tags = None
        else:
            source_tags = item["sourceTags"].split(",")
        source_ranges = []
        if item["sourceRanges"] == "":
            source_ranges = None
        else:
            for source in item["sourceRanges"].split(","):      
                source_ranges.append(QuotedString(source))
        destination_ranges = item["destinationRanges"]
        if destination_ranges == "":
            destination_ranges = None
        else:
            destination_ranges = destination_ranges.split(",")

        newfw_rule = {item["name"]: {
                    "description": item.get("description"),
                    "direction": item.get("direction"),
                    "disabled": str2bool(item["disabled"]),
                    "logging": str2bool(item.get("logging")),
                    "priority": item.get("priority"),
                    "rule": {
                        "allow": allowed_data,
                        "deny": denied_data,
                        "sourceRanges": source_ranges,
                        "destinationRanges": destination_ranges,
                        "sourceTags": source_tags,
                        "destinationTags": item.get("destinationTags"),
                        "sourceServiceAccounts": item.get("sourceServiceAccounts"),
                        "targetServiceAccounts": item.get("targetServiceAccounts"),
                        "targetTags": target_tags,
                    }
        }}
        cleanNullTerms(newfw_rule)
        pdata = yaml.dump(newfw_rule, Dumper=MyDumper, default_flow_style=False, allow_unicode=True)
        print(pdata)

if __name__ == "__main__":
    main()