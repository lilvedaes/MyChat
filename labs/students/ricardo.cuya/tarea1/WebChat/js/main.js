$(document).ready(function(){
	validUsername = "arturocuya";
	validPassword = "1234";
	errorContainer = $("#error-container");

	error_emptyField = '<p style="background-color: rgba(255,99,71,.1); color: tomato; padding: 5px; text-align: center;">Uno o más de los campos está vacío</p>';
	error_invalidCredentials = '<p style="background-color: rgba(255,99,71,.1); color: tomato; padding: 5px; text-align: center;">Credenciales incorrectas</p>';

	$("#btn-login").click(function(e) {
		username = $("#input-username").val();
		password = $("#input-password").val();
		if(username == "" || password == "") {
			errorContainer.html(error_emptyField);
		} else {
			if (username == validUsername && password == validPassword) {
				window.open("chat.html","_self");
			} else {
				errorContainer.html(error_invalidCredentials);
			}
		}
		e.preventDefault();
	});
});
