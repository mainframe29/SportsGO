from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class Cadastro_ou_login(BoxLayout):
    Builder.load_file('cadastro_ou_login_graph.kv')

class Principal(App):
    def build(self):
        return Cadastro_ou_login()

Principal().run()
