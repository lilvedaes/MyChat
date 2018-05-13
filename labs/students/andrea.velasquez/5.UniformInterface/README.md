# CSUTEC-CS2B01-B
### Tarea 5: API que permite gestionar mensajes.  

URI | Method | RQ Body | Result
-----------|-----------|-----------|-----------
/messages | GET | empty | returns all messages
/messages | POST | message (in JSON) | new message created
/messages/<id> | GET | empty | returns single message
/messages/<id> | PUT | message | message updated
/messages/<id> | DELETE | empty | message deleted

**Importante:** El URI **/** realiza la funcion _set_messages_ y redirige a la URI **/messages**, esto se debe realizar directamente en el buscador pues algunos REST API plugin no permiten la redirección.
