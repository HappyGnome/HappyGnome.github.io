# -*- coding: utf-8 -*-

import rule_prop_table as rpt
import json

rules_path="../docs/rules.json"
props_path="../docs/propositions.json"

rules=rpt.rule_prop_table("rules")
rules.default_item=rpt.rpi_rule_converter()

props=rpt.rule_prop_table("props")
props.default_item=rpt.rpi_prop_converter()

#try:
with open(rules_path,"r") as rules_file:
    data=json.load(rules_file)
    data["items"]=data["rules"]
    rules.from_dict(data)
#except:
    #print("Failed to load rules! Exiting...")
with open(props_path,"r") as props_file:
    data=json.load(props_file)
    data["items"]=data["propositions"]
    props.from_dict(data)
    


with open("../docs/rules_n.json","w") as rules_file:
    json.dump(rules.to_dict(),rules_file)

with open("../docs/props_n.json","w") as props_file:
    json.dump(props.to_dict(),props_file)
