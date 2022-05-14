import requests
from bs4 import BeautifulSoup

response = requests.get("http://google.com/")

print(" STATUS:" + str(response.status_code))
print(" CABECERAS:" + str(response.headers))

cuerpo_respuesta= response.content
if response.status_code == 200:
    html=BeautifulSoup(cuerpo_respuesta, "html.parser")

    print("---------------------")
    print(response.content)
   # print("---------------------------------------")
   # print(html.head)
    print("---------------------------------------")
    for meta in html.find_all('meta'):
        print(meta)
    print(html.head.name)
    print(html.head.meta)
    print(html.head.meta['content'])

    print("---------------------------------------")
    print(html.a)
    print(html.a.parent)
    print(html.a.parent.name)
    print(html.p.a.parent.name)

    print("---------------------------")
    for enlace in html.find_all('a'):
        print(enlace)
    print(enlace.string)
    print(enlace['href'])
    print(enlace.get('href'))

    print("--------------------------")










































