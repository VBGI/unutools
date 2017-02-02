
var equipmentFormStatus=false;

$(document).ready(function () {
var startdate = $("#main-equipment-form input[name*=starttime]").val();
$("#main-equipment-form input[name*=time]").datepicker();
$("#main-equipment-form input[name*=time]").datepicker("option", "dateFormat", 'yy-mm-dd');
$( "#main-equipment-form input[name*=time]" ).datepicker( "setDate", startdate);

$( "#main-equipment-form" ).submit(function( ev ) {
	
  alert( "Handler for .submit() called." );
  ev.preventDefault();
});

});


function showEquipmentList(){

$("#equipment-list-wrapper").load("{%url ""%}");

}


function resizable (el, factor) {
  var smint = Number(factor) || 8;
  function resize() {
  	var cval = $("#main-equipment-form input[id*=name]").val();
  	var cwid = $(el).width();
	if ((el.value.length + 1) * smint<500){
		el.style.width = (el.value.length + 1) * smint + 'px';	
	}

 if (!equipmentFormStatus&(cval.length>2)) {
  $("#equipment-form-wrapper").css("height", "100%");
  equipmentFormStatus=true;
  };
}
  	
  var e = 'keypress,change'.split(',');
  for (var i in e) el.addEventListener(e[i],resize,false);
  resize();
}

$.each($("#main-equipment-form input"), function(ind, obj){
	resizable(obj, 15);
});



