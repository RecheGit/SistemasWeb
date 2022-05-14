'''
####################################################################################################
# Alumno: Kepa Reche Urrutia                                                                       #
#Tarea: Cliente web que descarga a una carpeta del ordenador los PDF de la asignatura Sistemas Web #
####################################################################################################
'''
import requests
import urllib
import sys
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import base64
import os



metodo = 'GET'
uri = "http://egela.ehu.eus/"
cabeceras = {'Host': 'egela.ehu.eus'}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)


#Nos redirecciona a otra pagina

metodo = 'GET'
uri = respuesta.headers['Location']
cabeceras = {'Host': uri.split('/')[2]}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)


#Nos sigue redireccionando

metodo = 'GET'
uri = respuesta.headers['Location']
cabeceras = {'Host': uri.split('/')[2]}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo, allow_redirects=False)


#Ya hemos llegado al logger(200 OK)

#Tenemos que conseguir el logintoken, y la moodlesession

#Conseguimos el logintoken:
# Pasamos el contenido HTML de la web a un objeto BeautifulSoup
html = BeautifulSoup(respuesta.content , "html.parser")
logintoken = html.find('input', {'name': 'logintoken'}).get('value')
#Ya tenemos la logintoken, ahora falta la MoodleSessionEgela
#Las cookies estan en el header de la respuesta
moodlecookie=respuesta.headers['Set-Cookie'].split(';')[0]


#Hacemos el envio de los datos
metodo = 'POST'
#Enviamos tambien la cookie
cabeceras= {'Host':uri.split('/')[2], 'Content-Type': 'application/x-www-form-urlencoded','Cookie': moodlecookie}
cuerpo= {'logintoken': logintoken, 'username': "XXXX", 'password' : "XXXX"}
respuesta = requests.request(metodo, uri, data=cuerpo,headers=cabeceras, allow_redirects=False)
moodlecookie=respuesta.headers['Set-Cookie'].split(';')[0]#Obtenemos la nueva cookie
#Redireccion a otra pagina
metodo = 'GET'
uri = respuesta.headers['Location']
cabeceras = {'Host': uri.split('/')[2],'Cookie': moodlecookie}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

#Redireccion a otra pagina
metodo = 'GET'
uri = respuesta.headers['Location']
cabeceras = {'Host': uri.split('/')[2],'Cookie': moodlecookie}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)


#Ya estamos en la pagina de Egela

#Buscamos Sistemas Web dentro del HTML de egela y obtenemos el link a su clase

html = BeautifulSoup(respuesta.content, 'html.parser')
links_clases = html.find_all('a',{'class': 'ehu-visible'})

for asignaturas in links_clases:
    if asignaturas.text == "Sistemas Web":
        link_SistemasWeb=asignaturas.get('href')
        print(link_SistemasWeb)

#Hacemos una petición a la clase de Sistemas Web
metodo = 'GET'
uri = link_SistemasWeb
cabeceras = {'Host': uri.split('/')[2],'Cookie': moodlecookie}
cuerpo = ''
respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)


#Ya estoy dentro de SW
#PETICION para descargar los pdfs
html = BeautifulSoup(respuesta.content, 'html.parser')
cont=0
#Buscamos los links de los PDFs y hacemos una peticion con cada link
for link in html.find_all('a',{'class': 'aalink'}):
    src = link.find('img')['src']
    if str(src).endswith('pdf'):
        cont=cont+1
        link_pdf=link.get('href')#ontenemos el link al pdf
        #PETICION para descargar los pdfs
        metodo = 'GET'
        uri = link_pdf
        cabeceras = {'Host': 'egela.ehu.eus', 'Cookie': moodlecookie}
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

        #Tenemos que hacer otra peticion porque tenemos que loggearnos en egela
        metodo = 'GET'
        uri = respuesta.headers['Location']
        cabeceras = {'Host': uri.split('/')[2], 'Cookie': moodlecookie}
        cuerpo = ''
        respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
        #ahora descargamos y guardamos los pdfs
        os.makedirs("./pdf", exist_ok=True)
        pdf = open("./pdf/" + str(cont) + ".pdf", "wb")
        pdf.write(respuesta.content)
        pdf.close()
        print("PDF "+ str(cont) + " descargando...")

print("Descarga Exitosa, PDFs descargados y guardados correctamente en la carpeta PDF")










