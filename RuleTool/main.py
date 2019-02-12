# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 17:03:57 2019

@author: Ben
"""

import json
import subprocess as sp
import datetime


#load config or create it
config={"user":"", "sitepath":"", "editor":"notepad.exe"}

def cmdConfig(args):
    global config
    config["user"]=input("Enter username: ")
    config["sitepath"]=input("Enter local path to website data: ")
    config["editor"]=input("Text editor: ")
    try:
        with open("config.json","w") as config_file:
            json.dump(config,config_file)
    except:
        return False
    return True

try:
    with open("config.json","r") as config_file:
        config=json.load(config_file)
except:
        if not cmdConfig(None):
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

rules_by_label=None
props_by_label=None
def UpdateIndexByLabel():
    global rules_by_label, props_by_label
    rules_by_label=getIndexByLabel(rules["rules"])
    props_by_label=getIndexByLabel(props["propositions"])
UpdateIndexByLabel()

'''
##############################################################
CLI
##############################################################
'''
selection="" #user readable string for selected object label in cli
sel_mode="r"#"p" or "r" for proposition or rule
selected_id=""
selected_obj=None
selected_objlist=rules["rules"]#props or rules
selected_by_label=rules_by_label


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
    
def editText_paras(paras):#calls editText on text consisting of given paragraphs. 
#Parses output to return new list of paragraphs
    text=""
    for p in paras:
        text+=p+"\n\n"
    text=editText(text)
    
    ret=[]
    para=""
    for line in text.splitlines():
        if line.lstrip()=="":
            ret.append(para[:])
            para=""
        else:
            para+=line+"\n"
    if para!="":
        ret.append(para)#catch final paragraph
    return ret
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
    
def SetAuthorDate(obj):
    obj["author"]=config["user"]
    obj["date"]=str(datetime.date.today())
'''
************************************************************
Command handlers
'''
def cmdExit(args):
    return False
def cmdSave(args):
    SetAuthorDate(rules)
    SetAuthorDate(props)
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
    global selection, sel_mode, selected_id, selected_obj,  selected_objlist, selected_by_label
    if len(args)<1:#return to root
        selection=""
        selected_id=""
        selected_objlist=None
        selected_obj=None
        selected_by_label=None
        return True
    labeldata=toRulesLabel(args)
    if not labeldata: return True
    sel_mode=labeldata[0]
    label=labeldata[1]
    
    if sel_mode=='r':        
        if label in rules_by_label:
            selection=sel_mode+label   
            selected_objlist=rules["rules"]
            selected_id=rules_by_label[label] 
            selected_obj=selected_objlist[selected_id]
            selected_by_label=rules_by_label
    else:
        if label in props_by_label:
            selection=sel_mode+label
            selected_objlist=props["propositions"]
            selected_id=props_by_label[label]   
            selected_obj=selected_objlist[selected_id]
            selected_by_label=props_by_label
    return True



def cmdEdit_label(args):
    global selection
    if not selected_obj: return True
    st=input(" New label: ")
    if len(st)<1: return True
    if st in selected_by_label:
        b=input(" Warning! Label already in use. Continue (Y/N)? ")
        if not b in ["Y","y"]: 
            print(" Label not set.")
            return True 
    selected_obj["label"]=st
    selection=sel_mode+st
    UpdateIndexByLabel()
    print(" Label set.")
    return True
    
def cmdEdit_text(args):
    if not selected_obj: return True
    
    selected_obj["text"]=editText_paras(selected_obj["text"])
    return True
    
def cmdEdit_addnote(args):
    if not selected_obj: return True
    note={"content":editText("")}
    SetAuthorDate(note)
    selected_obj["notes"].insert(0,note)
    return True

def cmdEdit_setInEffect(args):
    if not selected_obj: return True
    if len(args)<1: return True
    
    if args[0] in ["Y","y"]:
        selected_obj["ineffect"]='1'
    else:
        selected_obj["ineffect"]='0'
        
    return True
    
edit_handlers={"l":cmdEdit_label, "t":cmdEdit_text, "na":cmdEdit_addnote, 
               "se":cmdEdit_setInEffect}
def cmdEdit(args):
    if len(args)<1: return True
    
    if args[0] in edit_handlers:
        return edit_handlers[args[0]](args[1:])
    return True

def cmdLink(args):
    if not selected_obj: return True
    label_data=toRulesLabel(args)
    if not label_data:
        print(" Linked item not found.")
        return True
    
    if label_data[0]=="r":
        if label_data[1] in rules_by_label:
            label_id=rules_by_label[label_data[1]]
            if not label_id in selected_obj["linksto"]:
                selected_obj["linksto"].append(label_id)
            if sel_mode=="r" and not selected_id in rules["rules"][label_id]["linksto"]:
                rules["rules"][label_id]["linksto"].append(selected_id)
            if sel_mode=="p" and not selected_id in rules["rules"][label_id]["proplinks"]:
                rules["rules"][label_id]["proplinks"].append(selected_id)
    elif label_data[0]=="p":
        if label_data[1] in props_by_label:
            label_id=props_by_label[label_data[1]]
            if not label_id in selected_obj["proplinks"]:
                selected_obj["proplinks"].append(label_id)
            if sel_mode=="r" and not selected_id in props["propositions"][label_id]["linksto"]:
                props["propositions"][label_id]["linksto"].append(selected_id)
            if sel_mode=="p" and not selected_id in props["propositions"][label_id]["proplinks"]:
                props["propositions"][label_id]["proplinks"].append(selected_id)
    
    return True
def cmdAdd(args):
    label_data=toRulesLabel(args)
    if not label_data: return True
    
    add_to_list=props["propositions"]
    if label_data[0]=="r":
        add_to_list=rules["rules"]           
    #find ID
    new_id=""
    j=len(add_to_list)
    while True:
        if not str(j) in add_to_list:
            new_id=str(j)
            break
        j=j+1
    add_to_list[new_id]={"ineffect":"1", "linksto":[], "notes":[], 
               "label":label_data[1], "proplinks":[], "text":""}
    date=input(" Date created (if not today): ")
    if date=="":
        date=str(datetime.date.today())
    add_to_list[new_id]["date"]=date
    
    if label_data[0]=="p":#author required
        auth=input(" Proposer name: ")
        add_to_list[new_id]["author"]=auth
        
    UpdateIndexByLabel()      
    return True

def cmdClear(args):
    global rules, props
    global selection, sel_mode, selected_id, selected_obj,  selected_objlist, selected_by_label
    b=input(" Warning! Clear all rules and propositions (Y/N)? ")
    if not b in ["Y","y"]: 
        print(" Nothing cleared - breathe!")
        return True 
    print(" Clearing...")
    rules={"rules":{}, "author":"", "date":""}
    props={"propositions":{}, "author":"", "date":""} 
    
    selection=""#clear selection
    selected_id=""
    selected_objlist=None
    selected_obj=None
    selected_by_label=None
    UpdateIndexByLabel()
    return True
'''
************************************************************
Main CLI cmd parser

return False to terminate main loop
'''
handlers={"quit":cmdExit,"save":cmdSave, "sel":cmdSel, 
          "edit":cmdEdit, "add":cmdAdd, "link":cmdLink, 
          "clear_all":cmdClear, "config":cmdConfig}# "del":cmdDel, ""}#define handlers
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