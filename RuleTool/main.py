# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 17:03:57 2019

@author: Ben
"""

import json;
import subprocess as sp;


#load config or create it
config={"user":"", "sitepath":"", "editor":"notepad.exe"}
try:
    with open("config.json","r") as config_file:
        config=json.load(config_file)
except:
    config["user"]=input("Enter username: ")
    config["sitepath"]=input("Enter local path to website data: ")
    config["editor"]=input("Text editor: ")
    try:
        with open("config.json","w") as config_file:
            json.dump(config,config_file)
    except:
        print("Failed to create config! Exiting...")
        exit(1)


#load json files for the website
rules=None;
props=None;
rules_path=config["sitepath"]+"rules.json"
props_path=config["sitepath"]+"propositions.json"

try:
    with open(rules_path,"r") as rules_file:
        rules=json.load(rules_file)
except:
    print("Failed to load rules! Exiting...")
    exit(1)

try:
    with open(props_path,"r") as props_file:
        props=json.load(props_file)
except:
    print("Failed to load propositions! Exiting...")
    exit(1)

'''
associate user-readable labels with ids
'''
def getIndexByLabel(arr):
    ret={}
    for a in arr:
        ret[arr[a]["label"]]=a
    return ret

rules_by_label=getIndexByLabel(rules["rules"])
props_by_label=getIndexByLabel(props["propositions"])

'''
##############################################################
CLI
##############################################################
'''
selection="" #user readable string for selected object label in cli
sel_mode="r"#"p" or "r" for proposition or rule
selected_obj_id=""

def editText(text):#open text editor and let user edit text, return edited version
    try:
        with open("temp.txt","w") as file:#create temp file
            file.write(text)
    except:
        print("Error creating file to edit!")
        return text
    try:
        proc=sp.Popen([config["editor"], "temp.txt"])
        proc.wait()
        with open("temp.txt","r") as file:#create temp file
            text=file.read()
        return text
    except:
        print("Error editing file!")
        return text
#convert e.g. ["pxyz\","abc", "dfg"] to ["p", "xyz abc", ind]
#ind=index of first argument not parsed
#or return None
def toRulesLabel(strings):
    if len(strings)<2 or not (strings[0]=="r" or strings[0]=="p"):
        return None
    ind=2
    st=strings[1]
    if st[-1]=='\\':
        st=st[:-1]+' '#strip trailing \
            
    for s in strings[2:]:
        ind+=1
        if len(s)<1:break
        elif s[-1]!='\\':
            st=st+s
            break
        else:
            st=st+s[:-1]+" "#strip trailing \
    return [strings[0][:],st,ind]  
    
'''
************************************************************
Command handlers
'''
def cmdExit(args):
    return False
def cmdSave(args):
    try:
        with open(rules_path,"w") as rules_file:
            json.dump(rules,rules_file)
        print(rules_path+" saved.")
    except:
        print("Saving "+rules_path+" did not complete successfully!")
    try:
        with open(props_path,"w") as props_file:
            json.dump(props,props_file)
        print(props_path+" saved.")
    except:
        print("Saving "+props_path+" did not complete successfully!")
    return True

def cmdSel(args):
    global selection, sel_mode, selected_obj_id
    if len(args)<1:#return to root
        selection=""
        selected_obj_id=""
        return True
    labeldata=toRulesLabel(args)
    if not labeldata: return True
    sel_mode=labeldata[0]
    label=labeldata[1]
    
    if sel_mode=='r':        
        if label in rules_by_label:
            selection="rule"+label            
            selected_obj_id=rules_by_label[label]
    else:
        if label in props_by_label:
            selection="prop"+label
            selected_obj_id=props_by_label[label]
    return True

def cmdEdit(args):
    
    
    return True
    
'''
************************************************************
Main CLI cmd parser

return False to terminate main loop
'''
handlers={"quit":cmdExit,"save":cmdSave, "sel":cmdSel, 
          "edit":cmdEdit}#, "add":cmdAdd, "del":cmdDel, "link":cmdLink, ""}#define handlers
def ParseCMD(cmd):
    toks=cmd.split()
    if len(toks)==0: return True#basic checks
    
    if toks[0] in handlers:
        return handlers[toks[0]](toks[1:])
    else: return True
    
    
'''
Main CLI loop
'''
while(True):
    cmd=input(selection+">")
    if not ParseCMD(cmd): break