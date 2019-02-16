$(document).ready(function(){	
	var dayIDstr=/[0-9]+/.exec(location.search);	
	if(dayIDstr){
		var dayID=parseInt(dayIDstr);
		$.when($.ajax({url:"days.json", type:"GET", dataType:"json"}),
		$.ajax({url:"rules.json", type:"GET", dataType:"json"}),
		$.ajax({url:"props.json", type:"GET", dataType:"json"}),
		$.ajax({url:"psoo.json", type:"GET", dataType:"json"}),
		$.ajax({url:"jdgmts.json", type:"GET", dataType:"json"})
		)
		.done(function(D,R,P,O,J){
			days=D[0];
			rules=R[0];
			props=P[0];
			psoo=O[0];
			jdgmts=J[0];//handles for data from ajax returns
			
			if (!(dayID in days.items)){
				$("#title").text("Day Not Found!");
				return;
			}
			var day=days.items[dayID];
			$("#title").text("Day "+day.label+ " Details");
			
			var sortedIds=[];
			for (var i=0; i<day.linksto["props"].length; i++){
				sortedIds.push(day.linksto["props"][i]);
			}
			sortedIds.sort(function(a,b){
				return props.items[a].label.localeCompare(props.items[b].label)});
				
			//load propositions##############################	
			for (var l=0; l<sortedIds.length; l++){		
				var prop=props.items[sortedIds[l]];			
				if(prop.ineffect=="1") $("#prop_list").append(GenerateRuleBox(props.items, sortedIds[l],{id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}));
				else $("#prop_list_repealed").append(GenerateRuleBox(props.items, sortedIds[l],{id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}));
			}
				
			var sortedIds=[];
			for (var i=0; i<day.linksto["psoo"].length; i++){
				sortedIds.push(day.linksto["psoo"][i]);
			}
			sortedIds.sort(function(a,b){
				return psoo.items[a].label.localeCompare(psoo.items[b].label)});	
			//Load psoo and judgements					
			for(var r=0;r<sortedIds.length;r++){
				$("#po_list").append(GeneratePOBox(psoo.items, sortedIds[r], jdgmts.items,{rule_lookup_url:"index.html",rule_name_lookup:rules.items}));
			}
				
		})
		.fail(function(){
			alert("Oops! Retrieval of data failed.");
		});	
	}
});