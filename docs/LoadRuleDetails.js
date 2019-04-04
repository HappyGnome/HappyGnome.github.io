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
			if(rule.ineffect=="1") $("#rules_list").append(GenerateRuleBox(rules.items,ruleID,"rule",true,true,"index.html",null,false,false));
			else $("#rules_list_repealed").append(GenerateRuleBox(rules.items,ruleID,"rule",true,true,"index.html",null,false, false));
			
			//load propositions##############################
			var bRepealedProps=false, bProps=false;
			
			//sort items ids by label
			var sortedIds=[];
			for (var i=0; i<rule.linksto["props"].length; i++){
				sortedIds.push(rule.linksto["props"][i]);
			}
			sortedIds.sort(function(a,b){
				return props.items[b].date.localeCompare(props.items[a].date)});
			
			for (var l=0; l<sortedIds.length; l++){		
				var prop=props.items[sortedIds[l]];			
				if(prop.ineffect=="1") {
					bProps=true;
					$("#prop_list").append(GenerateRuleBox(props.items, sortedIds[l],"prop",true,false,"index.html",rules.items,false, true));
				}
				else {
					bRepealedProps=true;
					$("#prop_list_repealed").append(GenerateRuleBox(props.items,sortedIds[l], "prop",true,false,"index.html",rules.items,false, true));
				}
			}
			if(bProps){
				$('#props_section').show();
			}
			if(bRepealedProps){
				$('#repealed_props_section').show();
			}
			
			MakeUsualCrossLinks();//complete partial anchor tags from json 
			
		})
		.fail(function(){
			alert("Oops! Retrieval of rules or props data failed.");
		});	
	}
});