# web-scraper

Código que obtiene datos de <a href='https://twitter.com/' target='_blank'>Twitter</a> a partir de un screen name.<br>
Los datos obtenidos son: fullname, bio description, total followers y avatar url.<br>
Se utiliza <a href='https://www.djangoproject.com/'>Django 1.11</a>, junto con las librerías <a href='http://www.django-rest-framework.org/'>django rest framwork</a> y <a href='https://www.crummy.com/software/BeautifulSoup/bs4/doc/' target='_blank'>BeautifulSoup</a> para el scraping.<br><br>


<strong>Instalación y prueba.</strong>

1 - Crear un entorno virtual:
<strong>virtualvenv vscraper</strong>

2 - Instalar los requerimientos:
<strong>pip install -requirements.txt</strong>

3 - Ejecutar las migraciones:
<strong>python manage.py migrate</strong>

4 - Ejecutar el servidor de prueba:
<strong>python manage.py runserver</strong>

5 - Abrir el navegador e ir a la siguiente URL:
<strong>http://localhost:8000/api/twitter/get_profile/?screen_name=reactjs</strong>
<br><br>
En este caso se mostrará el resultado para el screen_name "reactjs"<br><br>

<img src='https://image.ibb.co/eYOxz6/twitter_scraper2.png'>
