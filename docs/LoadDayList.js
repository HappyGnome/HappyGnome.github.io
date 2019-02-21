$(document).ready(function(){
	$.ajax({url:"days.json", type:"GET", dataType:"json"})
	.done(function(days){
		var sortedIds=[];
		for (var i in days.items){
			sortedIds.push(i);
		}
		sortedIds.sort(function(a,b){
			return days.items[b].date.localeCompare(days.items[a].date)});

		for (var d=0; d<sortedIds.length; d++){
			i=sortedIds[d];			
			var day=days.items[i];	
			S="<div class=\"daybox\">"
			S+="<a href=\"day_details.html?"+i+"\">"+day.label+" - "+day.date+"</a>"
			S+="</div>"
			$("#days_list").append(S);
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