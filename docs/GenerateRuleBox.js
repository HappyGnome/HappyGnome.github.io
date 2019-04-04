/*
Callback to show/hide notes section, given the id number of the rule
*/
function ToggleNotes(ruleID){
			$("#"+ruleID+" .rulefooter").toggle();
}

/*
Generate string for section of html document displaying a rule/proposal.

args: rules - list of rule items (from a json file)
- rule_key - index in rules of the item to render
- id_prefix - DOM id prefix of created section (usually "rule" or "prop")
- toggle_notes - boolean, true <=> display of associated notes may be toggled
- show_notes - boolean, true <=> associated notes shown by default
- rule_lookup_url - address of page where links to rules should lead to
- rule_name_lookup - list of rule items (where ids may be looked up)
- details - boolean, true <=> show details link
- show_author - boolean, true <=> show author attribution

return: [str, id]. str - string of html code for the generated section
id - DOM id of new section (once appended to the DOM)
*/
/*default arguments: "rule", true, false, "", null, true, false*/
function GenerateRuleBox(rules,rule_key,id_prefix/*="rule"*/, toggle_notes/*=true*/, show_notes/*=false*/, rule_lookup_url/*=""*/, rule_name_lookup/*=null*/, details/*=true*/, show_author/*=false*/){
	var rule=rules[rule_key];
	var dom_id=id_prefix+rule_key;
	var S="<section class=\"rulebox\" id=\""+dom_id+"\">"+
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
		S+=">"+rule.text;
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
	return [S+"</section>",dom_id];
}