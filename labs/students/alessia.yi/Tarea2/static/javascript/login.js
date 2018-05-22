function code(){
  var num = document.getElementById("password").value;
  document.getElementById("password").innerHTML = num;
    if (num==1234) {
      window.location='chat.html';

    } else {
      alert(document.getElementById("password").innerHTML = "Wrong Password");
    }
}
