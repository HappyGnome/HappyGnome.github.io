$(document).ready(function(){
	$.ajax({url:"days.json", type:"GET", dataType:"json"})
	.done(function(days){
		var sortedIds=[];	
		for (var i in days.items){
			sortedIds.push(i);
		}
		sortedIds.sort(function(a,b){
			var weekdelta=days.items[a].week-days.items[b].week
			if (weekdelta!=0){//sort by week first
				return -weekdelta;
			}
			else return days.items[b].date.localeCompare(days.items[a].date);});
			
		if(sortedIds.length>0){			
			var current_week=days.items[sortedIds[0]].week;
			$("#days_list").append("<h2>Week "+current_week+"</h2>");
			for (var d=0; d<sortedIds.length; d++){
				i=sortedIds[d];			
				var day=days.items[i];	
				
				if(day.week!=current_week){
					current_week=day.week;
					$("#days_list").append("<h2>Week "+current_week+"</h2>");
				}
				S="<div class=\"daybox\">"
				S+="<a href=\"day_details.html?"+i+"\">"+day.label+" ("+day.date+ ") "+day.desc+"</a>"
				S+="</div>"
				$("#days_list").append(S);
			}
		}
		//refresh hash:
		var hash=location.hash;
		location.hash="";
		location.hash=hash;
	})
	.fail(function(){
		alert("Oops! Retrieval of rules data failed.");
	});	
});