import json
import os
from datetime import datetime

from mycroft import MycroftSkill, intent_file_handler

# Fichero JSON donde almacenar la informacion
ficheroJSON = "/home/serggom/scraping/datos.json"


class EventosHoyCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.hoy.eventos.intent')
    def handle_campus_hoy_eventos(self, message):

        # Lectura de la informacion del fichero JSON
        if os.path.exists(ficheroJSON):

            # Lectura de la informacion del fichero JSON
            with open(ficheroJSON) as ficheroEventos:
                data = json.load(ficheroEventos)
                if len(data['eventos']) > 0:
                    now = datetime.now()
                    if now.day < 10:
                        dia = "0" + str(now.day)

                    else:
                        dia = str(now.day)

                    if now.month < 10:
                        mes = "0" + str(now.month)

                    else:
                        mes = str(now.month)

                    fecha_de_hoy = dia + "/" + mes + "/" + str(now.year)

                    for event in data['eventos']:

                        if event['fecha'] == fecha_de_hoy:
                            hora = int(event['hora'].split(":")[0])
                            minuto = int(event['hora'].split(":")[1])

                            if (hora > now.hour) or ((hora == now.hour) and (minuto > now.minute)):
                                self.speak("Hoy a las " + event['hora'] + " tienes " + event['nombre'])

                else:
                    self.speak("Hoy no tienes ningún evento")

            ficheroEventos.close()

        else:
            self.speak("Lo siento, no dispongo de esa información")


def create_skill():
    return EventosHoyCampus()
