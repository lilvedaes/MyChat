

function validatePassword() {
    var x, text;

    //Get the value of input field with id="password"
    x= document.getElementById("password").value;

        if (x == "1234"){
            text="Correct Password";
            location.href = "ChatPage.html";
        }
        else {
            text="Incorrect Password";
        }
        document.getElementById("demo").innerHTML=text;
}