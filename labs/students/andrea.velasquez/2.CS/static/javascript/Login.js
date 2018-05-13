function main() {
  $("#signin").fadeIn(1000);

  //Toggle password visibility
  $("#checkpass").click(function() {
    if ($("#checkpass").is(':checked')) {
      $("#password").attr("type", "text");
    } else {
      $("#password").attr("type", "password");
    }
  });

  //Activate wrong password alert or go to Chat.html
  $("#loginbutton").click(function() {
    $("#wrongpass").hide();
    $("#wronguser").hide();

    if ($("#username").val() === "" || $("#username").val() !== "admin"){ $("#wronguser").slideDown(300); }
    else if ($("#password").val() == "123") { window.location.href = "/chat.html"; }
    else { $("#wrongpass").slideDown(300); }
  });


}
//Hidden elements
$("#signin").hide();
$("#wrongpass").hide();
$("#wronguser").hide();
//Call main when loaded
$(document).ready(main);
