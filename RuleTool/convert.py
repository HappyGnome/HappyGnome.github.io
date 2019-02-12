# -*- coding: utf-8 -*-

import rule_prop_table as rpt
import json

rules_path="rules_old.json"
props_path="propositions_old.json"

rules=rpt.rule_prop_table("rules")
rules.default_item=rpt.rpi_rule_converter()

props=rpt.rule_prop_table("props")
props.default_item=rpt.rpi_prop_converter()

#try:
with open(rules_path,"r") as rules_file:
    rules.from_dict(json.load(rules_file))
#except:
    #print("Failed to load rules! Exiting...")
with open(props_path,"r") as props_file:
    props.from_dict(json.load(props_file))
    


with open("rules_new.json","w") as rules_file:
    json.dump(rules.to_dict(),rules_file)

with open("props_new.json","w") as props_file:
    json.dump(props.to_dict(),props_file)
