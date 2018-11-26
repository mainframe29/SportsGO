from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

class Tarefas(Screen):
    Builder.load_file('barra_lateral.kv')
class Init(App):
    def build(self):
        
        return Tarefas()

Init().run()