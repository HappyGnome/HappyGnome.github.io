$(document).ready(function(){	
	var dayIDstr=/[0-9]+/.exec(location.search);	
	if(dayIDstr){
		var dayID=parseInt(dayIDstr);
		$.ajax({url:"days.json", type:"GET", dataType:"json"})
		.done(function(days){
			$.ajax({url:"rules.json", type:"GET", dataType:"json"})
			.done(function(rules){
				if (!(dayID in days.items)){
					$("#title").text("Day Not Found!");
					return;
				}
				var day=days.items[dayID];
				$("#title").text("Day "+day.label+ " Details");
				
				//load propositions while we render the psoo##############################
				$.ajax({url:"props.json", type:"GET", dataType:"json"})
				.done(function(props){
					
					for (var i=0; i<day.linksto["props"].length; i++){		
						var prop=props.items[day.linksto["props"][i]];			
						if(prop.ineffect=="1") $("#prop_list").append(GenerateRuleBox(props.items, day.linksto["props"][i],{id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}));
						else $("#prop_list_repealed").append(GenerateRuleBox(props.items, day.linksto["props"][i],{id_prefix:"prop",rule_lookup_url:"index.html",rule_name_lookup:rules.items,details:false, show_author:true}));
					}
					
				}).fail(function(){
					alert("Oops! Retrieval of proposition data failed.");
				});
				
				//Load psoo and judgements
				$.ajax({url:"psoo.json", type:"GET", dataType:"json"})
				.done(function(psoo){
					
					$.ajax({url:"jdgmts.json", type:"GET", dataType:"json"})
					.done(function(jdgmts){
					
						for (var i=0; i<day.linksto["psoo"].length; i++){		
							var po_key=day.linksto["psoo"][i];			
							$("#po_list").append(GeneratePOBox(psoo.items, po_key, jdgmts.items,{rule_lookup_url:"index.html",rule_name_lookup:rules.items}));
						}
					
					}).fail(function(){
						alert("Oops! Retrieval of judgements data failed.");
					});
					
				}).fail(function(){
					alert("Oops! Retrieval of points of order data failed.");
				});
				
			}).fail(function(){
				alert("Oops! Retrieval of rules data failed.");
				});
		})
		.fail(function(){
			alert("Oops! Retrieval of days data failed.");
		});	
	}
});