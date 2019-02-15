//TODO: sort rules, search.
$(document).ready(function(){
	$.ajax({url:"days.json", type:"GET", dataType:"json"})
	.done(function(days){
		for (var i in days.items){	
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