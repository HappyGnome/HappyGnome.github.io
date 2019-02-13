# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:33:00 2019

@author: Ben
"""
import dictable
import copy
    
class rule_prop_item(dictable.dictable):
    def __init__(self):
        self.date=""
        self.label=""
        self.linksto={}#props, rules etc
    def dictable_items(self):#return items to add to dictionary
        return ["date","label", "linksto"]
    def to_dict(self):
        return self.dictify()
    def from_dict(self, dct):
        self.un_dictify(dct)
        
class rpi_rule(rule_prop_item):
    def __init__(self):
        super().__init__()
         #new dictables
        self.text=[]
        self.decorator=""
        self.notes=[]
        self.ineffect='1'
        
        self.linksto={"rules":[], "props":[]}#props, rules etc
        
    def dictable_items(self):
        dictables=super().dictable_items()
        dictables.extend(["text","decorator","notes","ineffect"])
        return dictables
class rpi_prop(rule_prop_item):
    def __init__(self):
        super().__init__()
        #new dictables
        self.author=""
        self.text=[]
        self.notes=[]
        self.ineffect='1'
        
        #defaults
        self.linksto={"rules":[], "props":[]}#props, rules etc
    def dictable_items(self):
        dictables=super().dictable_items()
        dictables.extend(["author","text","notes","ineffect"])
        return dictables
        
class rpi_rule_converter(rpi_rule):
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
class rpi_prop_converter(rpi_prop):
    def __init__(self):
        super().__init__()
    def from_dict(self, dct):        
        self.author=dct["author"]
        self.date=dct["date"]
        self.text=dct["text"]
        self.label=dct["label"]
        self.notes=dct["notes"]
        self.linksto["rules"]=dct["linksto"]
        self.linksto["props"]=dct["proplinks"]
        

class rule_prop_table(dictable.dictable):
    #typestring should match label in linksto for rpis!
    def __init__(self, atype_string):
        #dictable
        self.author=""
        self.date=""
        
        #not dictable
        
        
        #other RPTs that items may refer to
        self.type_string=atype_string
        
        self.companions={atype_string:self}
        self.default_item=rule_prop_item()
        
        self.__items__={}
        
        self.__item_ids_by_label__={}
        
    def getDefaultCopy(self):
        return copy.deepcopy(self.default_item)
    def setAuthorDate(self, AD):
        self.author=AD["author"]
        self.date=AD["date"]
    def setCompanion(self, other):
        self.companions[other.type_string]=other
        other.companions[self.type_string]=self
    def dictable_items(self):
        return ["author","date"]
    def to_dict(self):
        ret=self.dictify()
        if ret:
            ret["items"]={key:self.__items__[key].to_dict() for key in self.__items__}
        return ret
    def from_dict(self, dct):
        self.un_dictify(dct)
        if "items" in dct:
            for k in dct["items"]:
                rp_item=self.getDefaultCopy()
                rp_item.from_dict(dct["items"][k])
                self.__items__[k]=rp_item
        self.updateItemsByLabel()
                
    #refresh item_ids_by_label. Call this after editing an item's label!
    def updateItemsByLabel(self):
        self.item_ids_by_label={}
        for a in self.__items__:
            if not self.__items__[a].label in self.item_ids_by_label:
                self.item_ids_by_label[self.__items__[a].label]=[a]
            else:
                self.item_ids_by_label[self.__items__[a].label].append(a)
                #print("Warning! Label "+self.__items__[a].label+ " is ambiguous!")
            
    #return a dict of elements in items with matching label, indexed by their id
    def getItemsByLabel(self,label):
        return {k:self.__items__[k] for k in self.item_ids_by_label.get(label,[])}
    
    def addItem(self, item):
        #pick ID
        j=len(self.__items__)
        while True:
            if not str(j) in self.__items__:
                 break
            j=j+1
        self.__items__[str(j)]=item
        self.updateItemsByLabel()
    
    def addDefaultItem(self,label):
        #pick ID
        item=self.default_item()
        item.label=label
        self.add(item)
    
    def rmvItem(self, item_id):
        try:
            item=self.__items__[item_id]#break all links
            for L in item.linksto:
                for l in item.linksto[L]:
                    self.breakLink(item_id,l,L)
            
            self.__items__.pop(item_id)
            self.updateItemsByLabel()
        except KeyError:
            print("Item not found!")
        #TODO: unmake links
    
    def clear_all(self):
        for k in self.__items__:
            self.rmvItem(k)
    '''
    attempt to make a link between self.__items__[item_id]
    and self.companions[linked_item_in].items[linked_id]
    return True on success
    '''
    def makeLink(self, item_id, linked_id, linked_item_in):
        try:
            item_here=self.__items__[item_id]
            rpt=self.companions[linked_item_in]
            linksback=rpt.__items__[linked_id].linksto[self.type_string]
            if not item_id in linksback:
                linksback.append[item_id]
            linksfwd=item_here.linksto[linked_item_in]
            if not linked_id in linksfwd:
                linksfwd.append[linked_id]                
            
            return True
        except KeyError:
            print("Could not make link!") 
            return False
    
    '''
    attempt to break linksbetween self.__items__[item_id]
    and self.companions[linked_item_in].items[linked_id]
    return True on success
    '''
    def breakLink(self, item_id, linked_id, linked_item_in):
        try:
            item_here=self.__items__[item_id]
            rpt=self.companions[linked_item_in]
            linksback=rpt.__items__[linked_id].linksto[self.type_string]
            rpt.__items__[linked_id].linksto[self.type_string]=[l for l in linksback if l!=item_id]
            
            linksfwd=item_here.linksto[linked_item_in]
            item_here.linksto[linked_item_in]=[l for l in linksfwd if l!=linked_id]     
            
            return True
        except KeyError:
            print("Could not make link!") 
            return False
        
        
    
    
    
    
    
    
    
    
'''testing'''

#rpt=rule_prop_table()
#rpt.from_dict({"date": "2019-02-12", "items": {"16": {"text": ["Rule-changes that affect rules needed to allow or apply rule-changes are as permissible as other\nrule-changes. Even rule-changes that amend or repeal their own authority are permissible. No rule-change or type of move is impermissible solely on account of the self-reference or self-application\nof a rule.\n"], "date": "2019-02-11", "ineffect": "1", "label": "117", "author": "Initial", "notes": [], "linksto": ["16"], "proplinks": []}, "12": {"text": ["Immediately after a proposal is submitted in the proper fashion, players may cast their vote(s)\nwithin the Telegram voting thread. A vote is cast by replying with either the message \u201cVote: Yes\u201d\nor \u201cVote: No\u201d to support or disagree with the proposal. A vote may not be withdrawn. Any\nmessages sent after the player has already used their vote(s) are not counted towards the total.\n", "Voting is completed at the end of the day the proposal was submitted. After this point players may\nnot vote on the proposal.\n", ""], "date": "2019-02-11", "ineffect": "1", "label": "113", "author": "Initial", "notes": [], "linksto": ["12"], "proplinks": []}}, "author": "Ben"})
#d=rpt.to_dict()
