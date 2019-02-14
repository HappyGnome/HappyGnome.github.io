function ToggleNotes(ruleID){
			$("#"+ruleID+" .rulefooter").toggle();
}
function GenerateRuleBox(rules,rule_key,{id_prefix="rule", toggle_notes=true, show_notes=false, rule_lookup_url="", rule_name_lookup=null, details=true, show_author=false}={} ){
	var rule=rules[rule_key];
	var S="<section class=\"rulebox\" id=\""+id_prefix+rule_key+"\">"+
			"<div class=\"rulehead\"><h1>"+
				rule.label;
				if('decorator' in rule && rule.decorator!=""){
					S+="["+rule.decorator+"]";
				}
				S+="</h1>";
				if(details)S+="<div class=\"detail_link\">[<a href=rule_details.html?"
		+rule_key+">details</a>]</div>";
		S+="<div class=\"subhead\">";
		if(show_author) S+=" - "+rule.author+" - ";		
		S+=rule.date+"</div></div><div class=\"rulebody\" ";
		if(toggle_notes) S+="onclick=\"ToggleNotes('"+id_prefix+rule_key+"')\"";
		S+=">";
		for (var i=0; i<rule.text.length; i++)
		{
			S+="<p>"+rule.text[i]+"</p>";
		}
		S+="</div>";
		if(rule.notes.length || rule.linksto["rules"].length){
			S+="<div class=\"rulefooter\"";
			if(!show_notes)S+="style=\"display:none;\"";
			S+=">";
			if(rule.linksto["rules"].length){//C.F.		
				S+="<div class=\"cf\"> <i>c.f. rules:</i>";
				for (var j=rule.linksto["rules"].length-1; j>=0; --j){
					var ind=rule.linksto["rules"][j];
					var label=""
					if(rule_name_lookup){//look in external rule list if given
						label=rule_name_lookup[ind].label;						
					}
					else label=rules[ind].label;
					S+="<a href=\""+rule_lookup_url+"#rule"+ind+"\">"+label+"</a> "
				}
				S+="</div>";
			}						
			S+="<ul>";//Notes
			for (var j=rule.notes.length-1; j>=0; --j){
				var note=rule.notes[j];
				S+="<li class=\"footnote\">"+note.content+"<span class=attrib> - "+note.author+" "+note.date+"</span></li>";
			}
			S+="</ul></div>";
		}
	return S+"</section>";
}