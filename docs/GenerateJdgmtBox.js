/*
Generate string for section of html document displaying a judgement.

args: jdgmts - list of judgement items (from a json file)
- jdgmt_key - index in jdgmts of the item to render
- id_prefix - DOM id prefix of created section
- rule_lookup_url - address of page where links to rules should lead to
- rule_name_lookup - list of rule items (where ids may be looked up)

return: [str, id]. str - string of html code for the generated section
id - DOM id of new section (once appended to the DOM)
*/
function GenerateJdgmtBox(jdgmts,jdgmt_key, id_prefix/*="jdgmt"*/, rule_lookup_url/*=""*/, rule_name_lookup/*=null*/){
	var jdgmt=jdgmts[jdgmt_key];
	var S="<section class=\"jdgmtbox";
	var dom_id=id_prefix+jdgmt_key;
	if (jdgmt.overruled=="1")S+=" jdgmtdisp";
	S+="\" id=\""+dom_id+"\">"+
		"<div class=\"jdgmthead\"><h1>"+
			jdgmt.label+"</h1>";
	S+="<div class=\"subhead\">";
	S+=" - "+jdgmt.author+" - ";		
	S+=jdgmt.date+"</div></div><div class=\"jdgmtbody\" >"+jdgmt.text;
	S+="</div><div class=\"footer\">";
	
	S+="<ul>";//Notes
	for (var j=jdgmt.notes.length-1; j>=0; --j){
		var note=jdgmt.notes[j];
		S+="<li class=\"footnote\">"+note.content+"<span class=attrib> - "+note.author+" "+note.date+"</span></li>";
	}
	S+="</ul>"
		
	return [S+"</div></section>",dom_id];
}