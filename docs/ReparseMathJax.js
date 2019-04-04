/*
Test whether MathJax is available and if so, schedule the DOM item with given id to be processed by MathJax
*/
function ReparseMathJax(dom_id){
	try{
		MathJax.Hub.Queue(["Typeset", MathJax.Hub, dom_id]);
	}
	catch(e){
		console.log("Failed to schedule MathJax reparse of "+dom_id);
	}
}