function TogglePOjdgmts(poID){
			$("#"+poID+" .jdgmt_list").toggle();
}
function GeneratePOBox(psoo,po_key, jdgmts,{id_prefix="po", toggle_jdgmts=true, show_jdgmts=false, rule_lookup_url="", rule_name_lookup=null}={} ){
	var po=psoo[po_key];
	var S="<section class=\"pobox\" id=\""+id_prefix+po_key+"\">"+
			"<div class=\"pohead\"><h1>"+
				po.label+"</h1>";
		S+="<div class=\"subhead\">";
		S+=" - "+po.author+" - ";		
		S+=po.date+"</div></div><div class=\"pobody\" ";
		if(toggle_jdgmts) S+="onclick=\"TogglePOjdgmts('"+id_prefix+po_key+"')\"";
		S+=">";
		for (var i=0; i<po.text.length; i++)
		{
			S+="<p>"+po.text[i]+"</p>";
		}
		S+="</div>"
		if(po.notes.length){
			S+="<div class=\"footer\">";
		
		/*if(po.linksto["rules"].length){//C.F.		
			S+="<div class=\"cf\"> <i>c.f. rules:</i>";
			for (var j=po.linksto["rules"].length-1; j>=0; --j){
				var ind=po.linksto["rules"][j];
				var label=""
				if(rule_name_lookup){//look in external rule list if given
					label=rule_name_lookup[ind].label;						
				}
				else label=po[ind].label;
				S+="<a href=\""+rule_lookup_url+"#rule"+ind+"\">"+label+"</a> "
			}
			S+="</div>";
		}*/
		
		
			S+="<ul>";//Notes
			for (var j=po.notes.length-1; j>=0; --j){
				var note=po.notes[j];
				S+="<li class=\"footnote\">"+note.content+"<span class=attrib> - "+note.author+" "+note.date+"</span></li>";
			}
			S+="</ul>";
			
			S+="</div>";
		}
		if(po.linksto["jdgmts"].length){
			S+="<div class=\"jdgmt_list\"";
			if(!show_jdgmts)S+="style=\"display:none;\"";
			S+=">";
			
			var sortedIds=[];
			for (var i=0; i<po.linksto["jdgmts"].length; i++){
				sortedIds.push(po.linksto["jdgmts"][i]);
			}
			sortedIds.sort(function(a,b){
				return jdgmts[a].label.localeCompare(jdgmts[b].label)});
			
			//judgements
			for (var j=0;j<sortedIds.length; j++){
				var jdgmtID=sortedIds[j];
				S+=GenerateJdgmtBox(jdgmts,jdgmtID,{rule_lookup_url:rule_lookup_url, rule_name_lookup:rule_name_lookup})		
				
			}
			S+="</div>";//jdgmt_list
		}
	
	return S+"</section>";
	
}