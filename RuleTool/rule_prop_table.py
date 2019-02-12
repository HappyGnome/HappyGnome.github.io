# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:33:00 2019

@author: Ben
"""
class dictable:    
    def dictable_items(self):
        return[]
    def dictify(self):
        items=self.dictable_items()
        return {key:getattr(self,key) for key in items}
#initialize dictable items
#found in given dictionary
    def un_dictify(self, dct):    
        items=self.dictable_items()
        for item in items:
            if item in dct:
                setattr(self,item,dct[item])
    
class rule_prop_item(dictable):
    def __init__(self):
        self.author=""
        self.date=""
        self.text=[]
        self.label=""
        self.decorator=""
        self.notes=[]
        self.ineffect=0
        self.linksto=[]
        self.proplinks=[]
    def dictable_items(self):#return items to add to dictionary
        return ["author","date","text","label","decorator","notes","ineffect",
                "linksto","proplinks"]
    def to_dict(self):
        return self.dictify()
    def from_dict(self, dct):
        self.un_dictify(dct)


class rule_prop_table(dictable):
    def __init__(self):
        self.author=""
        self.date=""
        self.items={}
    def dictable_items(self):
        return ["author","date"]
    def to_dict(self):
        ret=self.dictify()
        if ret:
            ret["items"]={key:self.items[key].to_dict() for key in self.items}
        return ret
    def from_dict(self, dct):
        self.un_dictify(dct)
        if "items" in dct:
            for k in dct["items"]:
                rp_item=rule_prop_item()
                rp_item.from_dict(dct["items"][k])
                self.items[k]=rp_item
                
'''testing'''
'''
rpt=rule_prop_table()
rpt.from_dict({"date": "2019-02-12", "items": {"16": {"text": ["Rule-changes that affect rules needed to allow or apply rule-changes are as permissible as other\nrule-changes. Even rule-changes that amend or repeal their own authority are permissible. No rule-change or type of move is impermissible solely on account of the self-reference or self-application\nof a rule.\n"], "date": "2019-02-11", "ineffect": "1", "label": "117", "author": "Initial", "notes": [], "linksto": ["16"], "proplinks": []}, "12": {"text": ["Immediately after a proposal is submitted in the proper fashion, players may cast their vote(s)\nwithin the Telegram voting thread. A vote is cast by replying with either the message \u201cVote: Yes\u201d\nor \u201cVote: No\u201d to support or disagree with the proposal. A vote may not be withdrawn. Any\nmessages sent after the player has already used their vote(s) are not counted towards the total.\n", "Voting is completed at the end of the day the proposal was submitted. After this point players may\nnot vote on the proposal.\n", ""], "date": "2019-02-11", "ineffect": "1", "label": "113", "author": "Initial", "notes": [], "linksto": ["12"], "proplinks": []}}, "author": "Ben"})
d=rpt.to_dict()
'''