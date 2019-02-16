$(document).ready(function(){	
	var ruleIDstr=/[0-9]+/.exec(location.search);	
	if(ruleIDstr){
		var ruleID=parseInt(ruleIDstr);
		$.when($.ajax({url:"rules.json", type:"GET", dataType:"json"}),
		$.ajax({url:"props.json", type:"GET", dataType:"json"}))
		.done(function(R, P){
			rules=R[0];
			props=P[0];//extract data part of ajax returns
			if (!(ruleID in rules.items)){
				$("#title").text("Rule Not Found!");
				return;
			}
			var rule=rules.items[ruleID];
			$("#title").text("Rule "+rule.label+ " Details");
			
			//generate rulebox#################################################
			if(rule.ineffect=="1") $("#rules_list").append(GenerateRuleBox(rules.items,ruleID,{show_notes:true,rule_lookup_url:"index.html",details:false}));
			else $("#rules_list_repealed").append(GenerateRuleBox(rules.items,ruleID,{show_notes:true,rule_lookup_url:"index.html",details:false}))
			
			//load propositions##############################
			for (var i=0; i<rule.linksto["props"].length; i++){		
				var prop=props.items[rule.linksto["props"][i]];			
				if(prop.ineffect=="1") $("#prop_list").append(GenerateRuleBox(props.items, rule.linksto["props"][i],{id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}));
				else $("#prop_list_repealed").append(GenerateRuleBox(props.items,rule.linksto["props"][i], {id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}))
			}
			
			
		})
		.fail(function(){
			alert("Oops! Retrieval of rules or props data failed.");
		});	
	}
});