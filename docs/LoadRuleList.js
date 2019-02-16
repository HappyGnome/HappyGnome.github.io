$(document).ready(function(){
	$.ajax({url:"rules.json", type:"GET", dataType:"json"})
	.done(function(rules){
		$("#title_annot").text("updated: " + rules.date +" by "+ rules.author);
		//sort items ids by label
		labelmap=[];
		for (var i in rules.items){
			labelmap.push([rules.items[i].label,i]);
		}
		labelmap.sort(function(a,b){return a[0].localeCompare(b[0])});
		var bRepealedRule=false;
		for (var l=0; l<labelmap.length;l++){//sort
			console.log(l);
			var i=labelmap[l][1];
			var rule=rules.items[i];			
			if(rule.ineffect=="1") $("#rules_list").append(GenerateRuleBox(rules.items, i));
			else {
				bRepealedRule=true;
				$("#rules_list_repealed").append(GenerateRuleBox(rules.items,i));
			}
		}
		if(bRepealedRule) $('#repealed_section').show();
		
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