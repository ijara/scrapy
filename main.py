import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_allowed_by_robots(url):
    # Get the base URL
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc

    # Get the robots.txt URL
    robots_url = urljoin(base_url, '/robots.txt')

    try:
        # Fetch the robots.txt content
        robots_content = requests.get(robots_url).text

        # Check if the User-agent is allowed to access the given URL
        return 'User-agent: *\nDisallow:' not in robots_content

    except requests.exceptions.RequestException:
        # If there is an error fetching robots.txt, assume it's allowed
        return True

def scrape_page(url):
    # Realizar la solicitud HTTP
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Verificar si el acceso está permitido según robots.txt
        if is_allowed_by_robots(url):
            # Parsear el contenido HTML de la página con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Aquí puedes comenzar a extraer la información que necesitas
            # Por ejemplo, si quieres obtener todos los enlaces de la página:
            enlaces = soup.find_all('a')

            for enlace in enlaces:
                print(enlace.get('href'))

        else:
            print(f'Acceso no permitido por robots.txt para {url}')

    else:
        print(f'Error al hacer la solicitud HTTP. Código de estado: {response.status_code}')

# URL de la página que quieres hacer scraping
url = 'https://www.ejemplo.com'

# Verificar si el acceso está permitido según robots.txt antes de hacer scraping
if is_allowed_by_robots(url):
    scrape_page(url)
else:
    print(f'Acceso no permitido por robots.txt para {url}')
