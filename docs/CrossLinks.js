//e.g. for elements of class a_rule pre-pend a string to href (assumed to just be an ID number when first loaded)
function MakeCrossLinks_type(cssClass, URLprefix){
	$("."+cssClass).each(function(){
		$(this).attr("href", URLprefix+$(this).attr("href"))
	});
}
//Wrapper for DoMakeUsualCrossLinks, update some default arguments
//otions_in={cssClass:"url",...}
function MakeUsualCrossLinks(options_in){
	options={a_rule:"index.html#rule", a_prop:"", a_day:"day_details.html?", a_po:"", a_jdgmt:""};//defaults
	for (k in options_in){//update from arguments
		options[k]=options_in[k];
	}
	DoMakeUsualCrossLinks(options);
}
//Call MakeCrossLinks_type for default types of link
//options={cssClass:"url",...}
function DoMakeUsualCrossLinks(options){
	for (a in options){
		console.log(a);
		MakeCrossLinks_type(a,options[a]);
	}		
}