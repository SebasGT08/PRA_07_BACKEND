from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

# Ruta al GeckoDriver
driver_path = "C:/webdrivers/geckodriver.exe"  # Cambia según tu configuración
service = Service(executable_path=driver_path)

# Función para limpiar comentarios
def clean_comment(comment):
    return comment.replace(";", "").replace("\n", " ")

# Función para extraer comentarios de un término de búsqueda con scroll
def extract_comments_from_topic(driver, topic, max_comments):
    print(f"Buscando comentarios para: {topic}")
    
    search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
    search_box.clear()
    time.sleep(random.uniform(2, 4))
    search_box.send_keys(topic)
    time.sleep(random.uniform(2, 4))
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(3, 5))

    comments = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(comments) < max_comments:
        # Extraer comentarios visibles
        tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
        for tweet in tweets:
            if len(comments) >= max_comments:
                break  # Detener si ya tenemos suficientes comentarios
            comments.add(tweet.text)

        if len(comments) >= max_comments:
            break  # Detener si ya tenemos suficientes comentarios

        # Hacer scroll hacia abajo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))  # Esperar a que se carguen nuevos tweets

        # Calcular la nueva altura de la página
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Detener si no hay más contenido para hacer scroll
        last_height = new_height

    return list(comments)[:max_comments]  # Asegurarse de no exceder el máximo de comentarios

# Función principal para obtener comentarios de Twitter
def get_x_comments(presidente, tema, max_comments):
    # Configuración inicial del navegador
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get("https://twitter.com/login")
        time.sleep(5)

        # Credenciales (reemplaza con tus credenciales)
        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys("gamessebax@gmail.com")  # Reemplaza con tu usuario
        time.sleep(random.uniform(2, 4))
        username_field.send_keys(Keys.RETURN)
        time.sleep(5)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("clave1234")  # Reemplaza con tu contraseña
        time.sleep(random.uniform(2, 4))
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # Construir la consulta de búsqueda
        query = f"{presidente} {tema} -filter:links lang:es"
        comments = extract_comments_from_topic(driver, query, max_comments)

        return comments
    except Exception as e:
        print(f"Error al obtener comentarios de Twitter: {e}")
        return []
    finally:
        driver.quit()