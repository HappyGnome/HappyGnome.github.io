var prev_scroll=0;
$(window).scroll(function(){
	var new_scroll=$('html, body').scrollTop();
	if (new_scroll<window.prev_scroll) $("nav").css("top","0px");
	else $("nav").css("top","-30px");
	window.prev_scroll=new_scroll;
});