import requests
from bs4 import BeautifulSoup

def get_elements_from_page(url):
# * realizar la peticion GET a la url.
    initial_response = requests.get(url);

# * Extraer el contenido de la pagina en un html.
    initial_soup = BeautifulSoup(initial_response.text, features="html.parser")

# * obtener todas las etiquetas <a>
    etiquetas_a = initial_soup.find_all('a', href=True)

    hrefs = []

# * Obtener los hrefs de las etiquetas a, limitandolo a 10 para reducir el tiempo de espera y verificar que sea url HTTP.
    for a  in etiquetas_a:
        if a["href"] not in hrefs and len(hrefs) < 10 and a["href"].startswith("http"):
            hrefs.append(a["href"])

# * Realizar un GET a cada url de la pagina original.
    result = {}
    for link in hrefs:
        if link not in result:
            sub_pages = requests.get(url)
            sub_soups = BeautifulSoup(sub_pages.text, features="html.parser")
            h1_p_list = sub_soups.find_all(["h1","p"])

            result[link]=[h1_p_list]

    return result

# * URL de prueba
url = "https://www.mercadolibre.com.ar/c/autos-motos-y-otros#menu=categories"

# * llamdo a la funcion
print(get_elements_from_page(url))