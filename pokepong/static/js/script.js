$(function(){
	$("#sub1, #sub2, #rand").button().css(
		{"margin":'5px',"margin-bottom":'10px'}	
	);
});
$(document).ready(function(){
	$("#rand").click(function(){
		randomize()
	});
	$("#sub1").click(function(){
		submit()
	});
	$("#sub2").click(function(){
		submit()
	});
});
