# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 16:51:42 2019

Miscelaneous utils

@author: Ben
"""

#look for named attribute in obj, or obj[attr] and return the result
#return None if not found as attr or entry
def getAttrOrValue(obj, attr):
    try:#try as attribute
        return getattr(obj,attr)
    except:#try as dict entry
        try:
            return obj[attr]
        except:
            return None
        
#look for named attribute in obj, or obj[attr] and return the result
#return None if not found as attr or entry
def setAttrOrValue(obj, attr, val):
    try:#try as attribute
        setattr(obj,attr,val)
    except:#try as dict entry
        try:
            obj[attr]=val
        except:
            return

'''
Recursively seek obj.strings[0].srings[1]....
Or the equivalent mixture of attribute and dictionary/list lookup, e.g.
 obj[strings[0]].srings[1]....
If strings[n]='*' then  obj.strings[0].srings[1]....strings[n-1] should be 
a list or implement .items, then all instances of
 obj.strings[0].srings[1]....strings[n-1].strings[n+1] will be searched
 
Replace exact matches of <find> with <replace> in all sought items at final level
if substr, replace instances of find as substring (now whole-string match)

Any dictionary items with key '*' cannot be searched for in this way

return number of replacements
'''             
def repl(obj, strings,find, replace, substr=False):
        if len(strings)<1: return 0
        rep_count=0
        if len(strings)>1:
            if strings[0]=='*':
                try:
                    for (key,val) in obj.items():
                        rep_count+=repl(val,strings[1:],find,replace,substr)
                except:
                    try:
                        for i in range(len(obj)):
                            rep_count+=repl(obj[i],strings[1:],find,replace,substr)
                    except:
                        return 0
            else: 
                atr=getAttrOrValue(obj,strings[0])
                rep_count+=repl(atr,strings[1:],find,replace,substr)
        else:#len(strings)==1
            if strings[0]=='*':#last character is wild
                try:
                    for (key,val) in obj.items():
                        if val==find:
                            obj[key]=replace
                            rep_count=1
                        elif substr:
                            s=obj[key].replace(find,replace)
                            if not s==obj[key]:rep_count=1
                            obj[key]=s
                except:
                    try:
                        for i in range(len(obj)):
                            if obj[i]==find:
                                obj[i]=replace
                                rep_count=1
                            elif substr:
                                s=obj[i].replace(find,replace)
                                if not s==obj[i]:rep_count=1
                                obj[i]=s
                                
                    except:
                        return 0
            else:
                try:
                    atr=getAttrOrValue(obj,strings[0])
                    if atr==find:
                        setAttrOrValue(obj,strings[0],replace)
                        rep_count=1
                    elif substr:
                        s=atr.replace(find,replace)
                        setAttrOrValue(obj,strings[0],s)
                        if not s==atr: rep_count=1
                except:
                    return 0
        return rep_count
            
'''
Testing
'''
'''
class TESTOBJ1:
    def __init__(self):
        self.a='A'
        self.b='D'
        self.c=[{'a':'A', 'b':'B'},{'a':'A', 'b':'B'}]
o1=[{'a':{'a':'A', 'b':'B'}, 'b':'B', 'c':{'b':'B','c':[{'a':'A', 'b':'B'},{'a':'A', 'b':'B'}]}}, 
     {'a':TESTOBJ1(), 'b':{'c':'A', 'b':'B'}, 'c':TESTOBJ1()}]
o2=[['1A','B1'],{'a':'1A','b':'B1'}]

repl(o1, ['*','a','b'],'B','X')
print(o1)#expect 0.a.b item changed to 'X' in first dict
print(o1[1]['a'].b)#still D

repl(o1, ['*','*','a'],'A','Y')
print(o1)#expect 0.a.a,  1.a.a,1.c.a item changed to 'Y' in first dict
print(o1[1]['a'].a)#now Y
print(o1[1]['c'].a)#now Y

repl(o1, ['*','c','*','*','*'],'B','Z')
print(o1)#expect 0.c.c.*['b']=Z
print(o1[1]['c'].c)#still [{'a':'A', 'b':'B'},{'a':'A', 'b':'B'}] 
repl(o1, ['*','c','c','*','*'],'B','Z')
print(o1)#expect 0.c.c.*['b']=Z
print(o1[1]['c'].c)#now [{'a':'A', 'b':'Z'},{'a':'A', 'b':'Z'}] 


repl(o2,['*','*'],'A','X',True)
repl(o2,['*','b'],'B','Y',True)#1[b] ="Y1", 0.0="1X"=1.a 
print(o2)
'''
