from kivy.app import App
import pymysql
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Principal(App):
    def build(self):
        box = BoxLayout(orientation='vertical')

        historia = Label(text= (str(self.get_history())+'\n'+str(self.get_rules())),font_size=15,size_hint=[.4,.4],pos_hint={'x':.25, 'y':.7},text_size=(930,None))
        
        nome = Label(text=str(self.get_name()),size_hint=[.2,.1],pos_hint={'x':.4},font_size=50)
        
        box.add_widget(nome)
        box.add_widget(historia)
        
        return box

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
