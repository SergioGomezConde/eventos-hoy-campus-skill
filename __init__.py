from mycroft import MycroftSkill, intent_file_handler


class EventosHoyCampus(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('campus.hoy.eventos.intent')
    def handle_campus_hoy_eventos(self, message):
        self.speak_dialog('campus.hoy.eventos')


def create_skill():
    return EventosHoyCampus()

