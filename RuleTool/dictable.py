# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 2019

@author: Ben
"""
class dictable:    
    def dictable_items(self):
        return[]
    def dictify(self):
        items=self.dictable_items()
        try:
            return {key:getattr(self,key) for key in items}
        except:
            return {}
#initialize dictable items
#found in given dictionary
    def un_dictify(self, dct):    
        items=self.dictable_items()
        for item in items:
            if item in dct:
                setattr(self,item,dct[item])
