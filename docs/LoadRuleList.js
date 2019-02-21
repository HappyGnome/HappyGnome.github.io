$(document).ready(function(){
	$.ajax({url:"rules.json", type:"GET", dataType:"json"})
	.done(function(rules){
		$("#title_annot").text("updated: " + rules.date +" by "+ rules.author);
		//sort items ids by label
		var sortedIds=[];
		for (var i in rules.items){
			sortedIds.push(i);
		}
		sortedIds.sort(function(a,b){
			return rules.items[a].label.localeCompare(rules.items[b].label)});
		var bRepealedRule=false;
		for (var l=0; l<sortedIds.length;l++){
			var i=sortedIds[l];
			var rule=rules.items[i];			
			if(rule.ineffect=="1") $("#rules_list").append(GenerateRuleBox(rules.items, i));
			else {
				bRepealedRule=true;
				$("#rules_list_repealed").append(GenerateRuleBox(rules.items,i));
			}
		}
		if(bRepealedRule) $('#repealed_section').show();
		
		MakeUsualCrossLinks();//complete partial anchor tags from json 
		
		//refresh hash:
		var hash=location.hash;
		if(hash){
			location.hash="";
			location.hash=hash.slice(1);
		}
	})
	.fail(function(){
		alert("Oops! Retrieval of rules data failed.");
	});	
});