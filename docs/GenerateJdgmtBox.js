function GenerateJdgmtBox(jdgmts,jdgmt_key, {id_prefix="jdgmnt", rule_lookup_url="", rule_name_lookup=null}={} ){
	var jdgmt=jdgmts[jdgmt_key];
	var S="<section class=\"jdgmtbox";
	if (jdgmt.overruled=="1")S+=" jdgmtdisp";
		S+="\" id=\""+id_prefix+jdgmt_key+"\">"+
		"<div class=\"jdgmthead\"><h1>"+
			jdgmt.label+"</h1>";
	S+="<div class=\"subhead\">";
	S+=" - "+jdgmt.author+" - ";		
	S+=jdgmt.date+"</div></div><div class=\"jdgmtbody\" >";
	for (var i=0; i<jdgmt.text.length; i++)
	{
		S+="<p>"+jdgmt.text[i]+"</p>";
	}
	S+="</div><div class=\"footer\">";
	
	/*if(jdgmt.linksto["rules"].length){//C.F.		
		S+="<div class=\"cf\"> <i>c.f. rules:</i>";
		for (var j=jdgmt.linksto["rules"].length-1; j>=0; --j){
			var ind=jdgmt.linksto["rules"][j];
			var label=""
			if(rule_name_lookup){//look in external rule list if given
				label=rule_name_lookup[ind].label;						
			}
			else label=jdgmt[ind].label;
			S+="<a href=\""+rule_lookup_url+"#rule"+ind+"\">"+label+"</a> "
		}
		S+="</div>";
	}*/
	
	S+="<ul>";//Notes
	for (var j=jdgmt.notes.length-1; j>=0; --j){
		var note=jdgmt.notes[j];
		S+="<li class=\"footnote\">"+note.content+"<span class=attrib> - "+note.author+" "+note.date+"</span></li>";
	}
	S+="</ul>"
		
	return S+"</div></section>";
}