from kivy.app import App
import pymysql
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder

class Tela(BoxLayout):
    Builder.load_file('esportedodia_graphics.kv')

    def hist_plus_rules(self):
        hist=str(self.get_history())+'\n'+str(self.get_rules())
        return hist
        
    def get_history(self):
        self.db = DbCon()

        texto=self.db.c.execute("select historia from esportes")
        texto = self.db.c.fetchone()

        return str(texto['historia'])

    def get_name(self):
        self.db = DbCon()
        texto = self.db.c.execute("select nome from esportes")
        texto = self.db.c.fetchone()

        return str(texto['nome'])
    def get_rules(self):
        self.db = DbCon()
        texto = self.db.c.execute("select regras from esportes")
        texto = self.db.c.fetchone()

        return str(texto['regras'])
class Principal(App):
    def build(self):
       return Tela()           

class DbCon:
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '',
                                  db = 'sports',
                                  charset = 'utf8mb4',
                                  cursorclass = pymysql.cursors.DictCursor)
        self.c = self.db.cursor()
        
Principal().run()
