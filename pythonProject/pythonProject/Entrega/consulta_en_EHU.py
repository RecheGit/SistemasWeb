import requests
import sys
import urllib

metodo = "POST"
uri = "https://www.ehu.eus/bilatu/buscar/bilatu.php?lang=es/processForm"
cabeceras = {"Host" : "https://www.ehu.eus/bilatu/buscar/bilatu.php?lang=es",
             "Content-Type" : "application/x-www-form-urlencoded"}
cuerpo = {"Apellidos/ Nombre": sys.argv[1]}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
print(cuerpo_encoded)

cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)

codigo = respuesta.status_code
descripción = respuesta.reason
print(str(codigo) + " " + descripción)
for cabecera in respuesta.headers:
    print(cabecera + ": " + respuesta.headers[cabecera])
cuerpo_respuesta = respuesta.content
print(respuesta.request.url)
print(cuerpo_respuesta)
