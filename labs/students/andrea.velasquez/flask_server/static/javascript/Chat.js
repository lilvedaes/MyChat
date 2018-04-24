function main(){
  $("body").fadeIn(1000);
  $("#welcome").click(function(){
    $("#welcome").fadeOut(1000);
  });


}




//Hidden elements
$("body").hide();
//Call main when loaded
$(document).ready(main);
