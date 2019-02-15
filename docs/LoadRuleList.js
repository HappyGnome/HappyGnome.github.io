$(document).ready(function(){
	$.ajax({url:"rules.json", type:"GET", dataType:"json"})
	.done(function(rules){
		$("#title_annot").text("updated: " + rules.date +" by "+ rules.author);
		for (var i in rules.items){		
			var rule=rules.items[i];			
			if(rule.ineffect=="1") $("#rules_list").append(GenerateRuleBox(rules.items, i));
			else $("#rules_list_repealed").append(GenerateRuleBox(rules.items,i))
		}
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