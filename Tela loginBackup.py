from kivy.app import App

import pymysql

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder

global id_session

class Tela(BoxLayout):
    Builder.load_file('telalogin_graphics.kv')
    
    def recebe(self):
        self.db = DbCon()
        recUsuario = self.boxUser.text
        recSenha = self.boxSen.text

        self.db.c.execute("select count(*),id_usu from usuario where nick = '"+str(recUsuario)+"' and senha = '"+str(recSenha)+"'") #coloca recUsuario na instrucao do banco
        test = self.db.c.fetchone() #busca uma linha

        
        if(test['count(*)'] == 1):
            self.confirma_login()
            id_session = test['id_usu']
            print(id_session)
        else:
            self.login_errado()
    def confirma_login(self):
        b = BoxLayout(orientation='vertical')

        aviso = Label(text='Login finalizado com sucesso')
        
        b.add_widget(aviso)

        pop = Popup(title='Login',content=b)
        pop.open()

    def login_errado(self):
        b = BoxLayout(orientation='vertical')
        
        voltar = Button(text='Voltar')
        aviso = Label(text='Usuario ou senha incorretos!!!')

        b.add_widget(aviso)
        b.add_widget(voltar)

        pop=Popup(title='Login',content=b)
        pop.open()
        voltar.bind(on_press=pop.dismiss)
    
class Principal(App):
    def build(self):
        return Tela()
    
##########################conexao com banco de dados
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
