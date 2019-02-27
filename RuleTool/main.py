# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 17:03:57 2019

@author: Ben
"""

import json
import subprocess as sp
import datetime
import rule_prop_table as rpt
import sys

#load config or create it
config={"user":"", "sitepath":"", "editor":"notepad.exe", "shortcuts":{}}
config_templates={}

def cmdConfig(args):
    global config
    config["user"]=input("Enter username: ")
    config["sitepath"]=input("Enter local path to website data: ")
    config["editor"]=input("Text editor: ")
    try:
        with open("config.json","w") as config_file:
            json.dump(config,config_file)
    except:
        print("Warning: Config not saved!")
    return True

def cmdSetShortcut(args):
    global config
    if len(args)<2: 
        if args and args[0]=="-l":
            for s in config["shortcuts"]:
                print("\"\\@"+s+"\" -> \""+config["shortcuts"][s]+"\"") 
        return True
    
    shortcuts=config["shortcuts"]
    text=ParseSlashEscaped(args[1])
    shortcuts.update({args[0]:text})  
    print("Shortcut added: \"\\@"+args[0]+"\" -> \""+text+"\"")      
    
    try:
        with open("config.json","w") as config_file:
            json.dump(config,config_file)
    except:
        print("Warning: Config not saved!")
    return True

try:#load config
    with open("config.json","r") as config_file:
        config.update(json.load(config_file))
except:
    if not cmdConfig(None):
        print("Failed to create config! Exiting...")
        sys.exit(1)

try:#load templates
    with open("templates.json","r") as template_file:
        config_templates.update(json.load(template_file))
except:
    print("No templates loaded!")

#load json files for the website
days=rpt.rule_prop_table("days")
days.default_item=rpt.rpi_day()

psoo=rpt.rule_prop_table("psoo")
psoo.default_item=rpt.rpi_po()

jdgmts=rpt.rule_prop_table("jdgmts")
jdgmts.default_item=rpt.rpi_jdgmt()

rules=rpt.rule_prop_table("rules")
rules.default_item=rpt.rpi_rule()

props=rpt.rule_prop_table("props")
props.default_item=rpt.rpi_prop()

rules.setCompanion(props)#link the two rpts
rules.setCompanion(psoo)#link the two rpts
rules.setCompanion(jdgmts)#link the two rpts
days.setCompanion(psoo)
days.setCompanion(props)
psoo.setCompanion(jdgmts)

tables={"r":rules, "p":props, "o":psoo, "d":days, "j":jdgmts}#handy for selecting an rpt based on user r/p/... switch
paths={"r":"rules", "p":"props", "o":"psoo", "d":"days", "j":"jdgmts"}
#css classes for links to particular objects on from tables
tables_class={"r":"a_rule", "p":"a_prop", "o":"a_po", "d":"a_day", "j":"a_jdgmt"}

for k in tables:
    t=tables[k]
    path=config["sitepath"]+paths[k]+".json"
    paths[k]=path
    try:
        with open(path,"r") as file:
            t.from_dict(json.load(file))
    except:
        print("Failed to load "+paths[k]+"!")
    


'''
##############################################################
CLI
##############################################################
'''
selection="" #user readable string for selected object label in cli
sel_mode="r"#"p" or "r" for proposition or rule
selected_id=""
selected_obj=None

date_of_new_items=""

def editText(text):#open text editor and let user edit text, return edited version
    text=DeParseSlashEscaped(text)
    try:
        with open("temp.txt","w") as file:#create temp file
            file.write(text)
    except:
        print("Error creating file to edit!")
        text=ParseSlashEscaped(text)
        return text
    try:
        proc=sp.Popen([config["editor"], "temp.txt"])
        proc.wait()
        with open("temp.txt","r") as file:#create temp file
            text=file.read()
        text=ParseSlashEscaped(text)
        return text
    except:
        print("Error editing file!")
        text=ParseSlashEscaped(text)
        return text
    
def editText_paras(paras):#calls editText on text consisting of given paragraphs. 
#Parses output to return new list of paragraphs
    text=""
    for p in paras:
        text+=p+"\n"
    text=editText(text)
    
    ret=[]
    para=""
    for line in text.splitlines():
        if line.lstrip()=="":
            if para!="":
                ret.append(para)
                para=""
        else:
            para+=line+"\n"
    if para!="":
        ret.append(para)#catch final paragraph
    return ret

#open text editor and let user edit text, return edited version
#Without parsing slash-escaped text
def editText_plain(text):
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

def previewText(text):#open text editor and let user edit text, return edited version
    try:
        with open("tempp.txt","w") as file:#create temp file
            file.write(text)
    except:
        print("Error creating file to preview!")
        return text
    try:
        sp.Popen([config["editor"], "tempp.txt"])
    except:
        print("Error previewing file!")
        return text

#convert '\\'-> '\' and '\_' to ' ' in string other characters following a \ are stripped
def ParseSlashEscaped(string):
    if len(string)<1: return ""
    repl={"\\":"\\","_":" "}#Do not add @ or # as keys!
    ret=""
    i=0
    while i<len(string):
        
        if string[i]=='\\':
            i+=1
            if i<len(string):
                strip_length=1#characters parsed following \\
                if string[i] in repl:
                    ret+=repl[string[i]]
                elif string[i]=='@':#shortcuts
                    tag=string[i:].split(None, 1)[0][1:]#get all between @ and whitespace
                    strip_length+=len(tag)+1#also consume first whitespace
                    ret+=config["shortcuts"].get(tag,'\\@'+tag)
                        
                elif string[i]=='#':#cross references: \#mode id  
                    sRem=string[i:]#remaining string
                    toks=sRem.split(None,3)#get all between # and whitespace
                    if len(toks)>2:#consume three toks (#mode, id, label)
                        print("Detected link to "+toks[0][1:]+" "+toks[1])
                        link=MakeHref(toks[0][1:], toks[1], toks[2])
                        if link:
                            ret+=link
                            strip_length=len(toks[0])#calculate total length of the 3 tokens+ space between
                            strip_length+=len(toks[1])+len(string[i+strip_length:].split(toks[1],1)[0])
                            strip_length+=len(toks[2])+len(string[i+strip_length:].split(toks[2],1)[0])
                            strip_length+=1
                        else:
                            ret+='\\#'
                    else:#not enough tokens - link is invalid, keep it and move on
                        ret+='\\#'
                        print("Link to "+toks[0]+" is missing specifiers!")
                    
                i+=strip_length
        else: 
            ret+=string[i]
            i+=1
    return ret

'''
partially undo parsing of slash-escaped string

Currently the only reversible escaped character is '\'.
Currently does not replace all spaces with \_

Return the result of de-parsing string
'''
def DeParseSlashEscaped(string):
    if len(string)<1: return ""
    repl={"\\":"\\\\"}#Do not add @ or # as keys!
    ret=""
    i=0
    while i<len(string):        
        s=repl.get(string[i],string[i])
        ret+=s
        i+=1
    return ret

'''
Return string containing html code for a link to the item with given label
(after resolution) in tables[mode]. Link text=label by default
'''
def MakeHref(mode, label, text="", auto_link=False) :
    text=ParseSlashEscaped(text)
    if not text: text=label#default value
    [item_id,mode_A2I,sel_string, sel_obj]=ArgsToID([mode,label])
    if not item_id:
        print("Linked item not found!")
        return ""
    
    if selected_obj and auto_link:#links items also in linksto
        tables[sel_mode].makeLink(selected_id,item_id,tables[mode_A2I].type_string)
    
    cssClass=tables_class.get(mode,"")
    if not cssClass:
        print("No valid href!")
        return ""
    #page will append appropriate string to the href to make a link
    return "<a href=\""+item_id+"\" class=\""+cssClass+"\">"+text+"</a>"

#convert e.g. ["p", "xyz\_abc", "dfg"] to ["p", "xyz abc"]
#or return None    
def toRulesLabel(strings):
    if len(strings)<2 or not (strings[0] in tables):
        return None
    st=ParseSlashEscaped(strings[1])
    return [strings[0][:],st]  

def getAuthorDate():
    return {"author":config["user"], "date":str(datetime.date.today())}
'''
************************************************************
Command handlers
'''
def cmdExit(args):
    return False
def cmdSave(args):
    for t in tables:#note who saves when!
        tables[t].setAuthorDate(getAuthorDate())
        try:
            with open(paths[t],"w") as file:
                json.dump(tables[t].to_dict(),file)
            print(paths[t]+" saved.")
        except:
            print("Saving "+paths[t]+" did not complete successfully!")
    return True

def ResolveID(items):
    if len(items)<1: return ["",""]
    if len(items)==1: return [list(items)[0],""]
    
    #Multiple items!
    preview_text=""
    i=0
    conv={}#{"i":"k"} pairs
    for k in items:
        preview_text+="############################_"+str(i)+"_############################\n"
        preview_text+=str(items[k].to_dict())+"\n"
        i+=1
        conv[str(i)]=k
    previewText(preview_text)    
    
    s=input("Please enter the number of the item to select: ")
    if s in conv:
        return [conv[s], "#"+s]
    return ["",""]

#return [resolved id,mode, selection_string, selected_object] from args ["mode","slash_escaped_label"]
#return ["",""] on failure
def ArgsToID(args):
    labeldata=toRulesLabel(args)
    if not labeldata: return ["","","",None]
    mode=labeldata[0]
    label=labeldata[1]
    
    if not mode in tables: 
        return ["","","",None]
    
    T=tables[mode]
    matched_items=T.getItemsByLabel(label)
    resolved=ResolveID(matched_items)
    if resolved[0]=="": return ["","","",None]
    return [resolved[0],mode,mode+label+resolved[1],matched_items[resolved[0]]]
  
def cmdSel(args):
    global selection, sel_mode, selected_id, selected_obj
    if len(args)<1:#return to root
        selection=""
        selected_id=""
        selected_obj=None
        return True
    
    [item_id,mode,sel_string, sel_obj]=ArgsToID(args)#prompt user to select an item by ID if there are more than one
    
    if item_id=="": return True
    
    sel_mode=mode
    selection=sel_string
    selected_id=item_id
    selected_obj=sel_obj
    
    return True

def cmdRm(args):
    global selection, sel_mode, selected_id, selected_obj
    
    [item_id,mode,sel_string, sel_obj]=ArgsToID(args)
    
    if item_id=="": return True
    if sel_obj==selected_obj:
        selection=""
        selected_id=""
        selected_obj=None
    
    tables[mode].rmvItem(item_id)
    
    return True



def cmdEdit_label(args):
    global selection
    if not selected_obj: return True
    st=input(" New label: ")
    if len(st)<1: return True
    if len(tables[sel_mode].getItemsByLabel(st))>0:
        b=input(" Warning! Label already in use. Continue (Y/N)? ")
        if not b in ["Y","y"]: 
            print(" Label not set.")
            return True 
    selected_obj.label=st
    selection=sel_mode+st
    tables[sel_mode].updateItemsByLabel()
    print(" Label set.")
    return True
    
def cmdEdit_text(args):
    if not selected_obj: return True
    
    if getattr(selected_obj,"text", None)!=None:
        selected_obj.text=editText_paras(selected_obj.text)
    return True
    
def cmdEdit_addnote(args):
    if not selected_obj: return True
    notes=getattr(selected_obj,"notes", None)
    if notes==None: return True
    
    text=""
    if len(args)>0:
        text=config_templates.get(args[0],"")
    note={"content":editText(text)}
    note.update(getAuthorDate())
    notes.insert(0,note)
    return True

def cmdSetTemplate(args): 
    global config_templates
    if len(args)<1:
        return True
    text=config_templates.get(args[0],"")
    text=editText_plain(text)
    
    config_templates[args[0]]=text
    
    try:
        with open("templates.json","w") as template_file:
            json.dump(config_templates,template_file)
    except:
        print("Warning: Template not saved!")
    
    return True
#return None, or the index of selected note
def GetNoteID():    
    if not selected_obj: return None
    notes=getattr(selected_obj,"notes", None)
    if notes==None or len(notes)<1: return None
    
    if len(notes)==1: return 0
    
    #Multiple items!
    preview_text=""
    for k in range(len(notes)):
        preview_text+="############################_"+str(k)+"_############################\n"
        preview_text+=str(notes[k])+"\n"
    previewText(preview_text)    
    
    try:
        s=int(input("Please enter the number of the note to select: "))
        if s>=0 and s<len(notes): return s
        else: return None
    except: 
        return None
    
    
def cmdEdit_editnote(args):
    ID=GetNoteID()
    if ID==None: return True
    
    note={"content":editText(selected_obj.notes[ID]["content"])}
    note.update(getAuthorDate())
    selected_obj.notes[ID]=note
    return True
def cmdEdit_rmnote(args):
    ID=GetNoteID()
    if ID==None: return True
    
    selected_obj.notes.pop(ID)
    return True

#flag is the name of a '0'/'1' string boolean attribute
def setFlag(args, flag):
    if not selected_obj: return True
    ie=getattr(selected_obj,flag, None)
    if ie==None: return True
    
    if len(args)<1: return True
    
    if args[0] in ["Y","y"]:
        setattr(selected_obj,flag,'1')
    else:
        setattr(selected_obj,flag,'0')      
    return True

def cmdEdit_setInEffect(args): 
    return setFlag(args,"ineffect")
def cmdEdit_setOverruled(args): 
    return setFlag(args,"overruled")

#convert first arg into attribute with given name, if it exists
def setString(args, atr):
    if not selected_obj: return True
    ie=getattr(selected_obj,atr, None)
    if ie==None: return True
    
    if len(args)<1: return True
    
    setattr(selected_obj,atr,ParseSlashEscaped(args[0]))      
    return True
def cmdSetAuth(args):
    return setString(args,"author")
def cmdSetDate(args):
    return setString(args,"date")
def cmdSetDecorator(args):
    return setString(args,"decorator")
    
edit_handlers={"l":cmdEdit_label, "t":cmdEdit_text, "na":cmdEdit_addnote, "ne":cmdEdit_editnote,
               "nr":cmdEdit_rmnote,
               "se":cmdEdit_setInEffect, "sovr":cmdEdit_setOverruled,
               "auth":cmdSetAuth, "date":cmdSetDate, "dec":cmdSetDecorator}
def cmdEdit(args):
    if len(args)<1: return True
    
    if args[0] in edit_handlers:
        return edit_handlers[args[0]](args[1:])
    else:
        print("Unrecognized edit command!")
    return True

def cmdLink(args):
    if not selected_obj: return True
    [item_id,mode,sel_string, sel_obj]=ArgsToID(args)
    if not item_id:
        print(" Linked item not found.")
        return True
    tables[sel_mode].makeLink(selected_id,item_id,tables[mode].type_string)
    return True
    
def cmdUnLink(args):
    if not selected_obj: return True
    [item_id,mode,sel_string, sel_obj]=ArgsToID(args)
    if not item_id:
        print(" Linked item not found.")
        return True
    tables[sel_mode].breakLink(selected_id,item_id,tables[mode].type_string)
    
    
    return True
def cmdAdd(args):
    label_data=toRulesLabel(args)
    if not label_data: return True
    
    item=tables[label_data[0]].getDefaultCopy();
    item.label=label_data[1]
    item.date=date_of_new_items
    
    tables[label_data[0]].addItem(item)   
    
    return True

def cmdClear(args):
    global rules, props
    global selection, sel_mode, selected_id, selected_obj,  selected_objlist, selected_by_label
    b=input(" Warning! Clear all rules and propositions (Y/N)? ")
    if not b in ["Y","y"]: 
        print(" Nothing cleared - breathe!")
        return True 
    print(" Clearing...")
    
    for k in tables:
        tables[k].clear_all()
    
    return True

def cmdSetAddDate(args):
    global date_of_new_items
    if len(args)<1: return True
    date_of_new_items=args[0]
    return True

#replace text in specified attribute accross all items
#args:attr_name find replace_with
#find and replace_with are \ escaped
def cmdRepl(args):
    if len(args)<2: return True
    substr=False
    inp=input("Replace substrings? (Y/N): ")
    substr=(inp in ["Y","y"])
    repl=""
    if len(args)>2: 
        repl=ParseSlashEscaped(args[2])
    find=ParseSlashEscaped(args[1])
    for l in tables:
        count=tables[l].repl(args[0],find,repl,substr)
        print("In "+l+" replaced: "+str(count))
    return True
    
    
'''
************************************************************
Main CLI cmd parser

return False to terminate main loop
'''
handlers={"quit":cmdExit,"save":cmdSave, "sel":cmdSel, 
          "ed":cmdEdit, "add":cmdAdd, "lk":cmdLink, "ulk":cmdUnLink,
          "clear_all":cmdClear, "config":cmdConfig, "rm":cmdRm,
          "date":cmdSetAddDate,
          "repl":cmdRepl, "shortcut":cmdSetShortcut, "template":cmdSetTemplate}# "del":cmdDel, ""}#define handlers
def ParseCMD(cmd):
    toks=cmd.split()
    if len(toks)==0: return True#basic checks
    
    if toks[0] in handlers:
        return handlers[toks[0]](toks[1:])
    else: 
        print("Unrecognized command!")
        return True
    
    
'''
Main CLI loop
'''
while(True):
    cmd=input(selection+">")
    if not ParseCMD(cmd): break