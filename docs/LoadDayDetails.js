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
				var new_section=GenerateRuleBox(props.items, sortedIds[l],"prop",true, false,"index.html",rules.items,false, true)
				if(prop.ineffect=="1") $("#prop_list").append(new_section[0]);
				else $("#prop_list_repealed").append(new_section[0]);
				ReparseMathJax(new_section[1]);//queue maths typesetting of new section, using its id
			}
				
			var sortedIds=[];
			for (var i=0; i<day.linksto["psoo"].length; i++){
				sortedIds.push(day.linksto["psoo"][i]);
			}
			sortedIds.sort(function(a,b){
				return psoo.items[a].label.localeCompare(psoo.items[b].label)});	
			//Load psoo and judgements					
			for(var r=0;r<sortedIds.length;r++){
				var new_section=GeneratePOBox(psoo.items, sortedIds[r], jdgmts.items,"po",true, true,"index.html",rules.items);
				$("#po_list").append(new_section[0]);
				ReparseMathJax(new_section[1]);//queue maths typesetting of new section, using its id
			}
			
			MakeUsualCrossLinks();//complete partial anchor tags from json 
				
		})
		.fail(function(){
			alert("Oops! Retrieval of data failed.");
		});	
	}
});