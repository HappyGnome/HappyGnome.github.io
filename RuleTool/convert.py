# -*- coding: utf-8 -*-

import rule_prop_table as rpt
import json

class rpi_rule_converter(rpt.rpi_rule):
    def __init__(self):    
        super().__init__()
    def from_dict(self, dct):        
        self.date=dct["date"]
        self.text=dct["text"]
        self.label=dct["label"]
        self.notes=dct["notes"]
        self.ineffect=dct["ineffect"]
        self.linksto["rules"]=dct["linksto"]
        self.linksto["props"]=dct["proplinks"]
class rpi_prop_converter(rpt.rpi_prop):
    def __init__(self):
        super().__init__()
    def from_dict(self, dct):        
        self.author=dct["author"]
        self.date=dct["date"]
        self.text=dct["text"]
        self.label=dct["label"]
        self.notes=dct["notes"]
        self.ineffect=dct["ineffect"]
        self.linksto["rules"]=dct["linksto"]
        self.linksto["props"]=dct["proplinks"]
class rpi_jdgmt_converter(rpt.rpi_jdgmt):
    def __init__(self):
        super().__init__()
    def from_dict(self,dct):
        super().from_dict(dct)
        self.overruled=dct["disputed"]
        
'''
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
    


with open("../docs/rules.json","w") as rules_file:
    json.dump(rules.to_dict(),rules_file)

with open("../docs/props.json","w") as props_file:
    json.dump(props.to_dict(),props_file)
'''

jdgmt_path="../docs/jdgmts.json"
jdgmts=rpt.rule_prop_table("jdgmts")
jdgmts.default_item=rpi_jdgmt_converter()

with open(jdgmt_path,"r") as jdgmts_file:
    data=json.load(jdgmts_file)
    data["items"]=data["items"]
    jdgmts.from_dict(data)
with open(jdgmt_path,"w") as jdgmts_file:
    json.dump(jdgmts.to_dict(),jdgmts_file)