import time

from mycroft import MycroftSkill, intent_file_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import date


def inicio_sesion(self):
    # Datos de acceso fijos
    usuario = 'e71180769r'
    contrasena = 'p5irZ9Jm4@9C#6WUaE!z9%@V'

    # Modo headless
    options = Options()
    options.headless = True
    options.add_argument("--windows-size=1920,1200")

    self.speak("Buscando la informacion...")

    # Acceso a pagina
    driver = webdriver.Chrome(options=options)
    driver.get('https://campusvirtual.uva.es/login/index.php')

    # Inicio de sesion
    driver.find_element(by=By.NAME, value='adAS_username').send_keys(usuario)
    driver.find_element(
        by=By.NAME, value='adAS_password').send_keys(contrasena)
    driver.find_element(by=By.NAME, value='adAS_submit').click()

    # Aceptar cookies
    driver.implicitly_wait(10)
    driver.find_element(
        by=By.XPATH, value='/html/body/div[1]/div/a[1]').click()

    return driver


def mesANumero(x):  # Funcion que devuelve el numero de mes introducido de manera escrita
    return{
        'enero': "01",
        'febrero': "02",
        'marzo': "03",
        'abril': "04",
        'mayo': "05",
        'junio': "06",
        'julio': "07",
        'agosto': "08",
        'septiembre': "09",
        'octubre': "10",
        'noviembre': "11",
        'diciembre': "12",
    }[x]


# Funcion para dar formato a una fecha y devolverla en la respuesta
def formatear_fecha(fecha_a_formatear):
    fecha_separada = fecha_a_formatear.split(", ")
    hora = fecha_separada[2]
    fecha_formateada = "A las " + hora
    return fecha_formateada


class EventosHoyCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.hoy.eventos.intent')
    def handle_campus_hoy_eventos(self, message):
        driver = inicio_sesion(self)

        # Acceso al dia actual en el calendario
        driver.get('https://campusvirtual.uva.es/calendar/view.php?view=day')

        # Obtencion de la lista de eventos del dia
        eventos_dia = driver.find_elements(by=By.CLASS_NAME, value='event')

        # Obtencion del numero de eventos del dia
        numero_eventos = len(eventos_dia)

        # Respuesta con los eventos del dia
        if numero_eventos == 0:
            self.speak("Hoy no tienes ningun evento")

        elif numero_eventos == 1:
            self.speak_dialog('Hoy tienes un evento')
            evento_dia = eventos_dia[0]
            self.speak(formatear_fecha(evento_dia.find_element(by=By.CLASS_NAME, value='col-11').text.split(
                " » ")[0]) + " tienes " + evento_dia.find_element(by=By.TAG_NAME, value='h3').text)

        else:
            self.speak_dialog('uva.hoy.eventos', data={
                'numero_eventos': numero_eventos})
            for evento_dia in eventos_dia:
                self.speak(formatear_fecha(evento_dia.find_element(by=By.CLASS_NAME, value='col-11').text.split(
                    " » ")[0]) + " tienes " + evento_dia.find_element(by=By.TAG_NAME, value='h3').text)


def create_skill():
    return EventosHoyCampus()

