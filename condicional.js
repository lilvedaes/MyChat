
function validation(){
	var uname = document.login.uname.value;
	var pwd = document.login.pwd.value;

	if (uname=="admin" && pwd=="admin"){
		return true
	}
	else if (uname!="admin" || pwd!="admin") {
	    alert("Usuario o contraseña incorrecta");
	    return false
	}
}
