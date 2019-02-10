function GenerateRuleBox(rules,rule_ind, toggle_notes=true, show_notes=false, rule_lookup="", details=true){
	var rule=rules[rule_ind];
	var S="<section class=\"rulebox\" id=\"rule"+rule.id+"\">"+
			"<div class=\"rulehead\"><h1>"+
				rule.label+"</h1>";
				if(details)S=S+"<div class=\"detail_link\">[<a href=rule_details.html?"
		+rule.id+">details</a>]</div>";
		S=S+"<div class=\"subhead\">"+rule.date+"</div></div><div class=\"rulebody\" ";
		if(toggle_notes) S=S+"onclick=\"ToggleNotes("+rule.id+")\"";
		S=S+">"+rule.text+"</div>";
		if(rule.notes.length || rule.linksto.length){
			S=S+"<div class=\"rulefooter\"";
			if(!show_notes)S=S+"style=\"display:none;\"";
			S=S+">";
			if(rule.linksto.length){//C.F.		
				S+="<div class=\"cf\"> <i>c.f. rules:</i>";
				for (var j=rule.linksto.length-1; j>=0; --j){
					var ind=rule.linksto[j];
					S+="<a href=\""+rule_lookup+"#rule"+rules[ind].id+"\"> "+rules[ind].label+"</a>"
				}
				S+="</div>";
			}						
			S=S+"<ul>";//Notes
			for (var j=rule.notes.length-1; j>=0; --j){
				var note=rule.notes[j];
				S=S+"<li class=\"footnote\">"+note.content+"<span class=attrib> - "+note.author+" "+note.date+"</span></li>";
			}
			S+="</ul></div>";
		}
	return S+"</section>";
}