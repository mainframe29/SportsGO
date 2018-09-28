from kivy.app import App

import pymysql

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout

global id_session
class Principal(App):
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
            
    def build(self):
        self.db = DbCon()
        box = BoxLayout(orientation = 'vertical')
        botao = Button(text = 'Entrar',on_press = self.recebe,font_size=30,size_hint = [.5,.4],pos_hint={'x' : 0.25})

        self.boxUser = TextInput(size_hint=[.5,.4],pos_hint={'x' : .25})
        self.boxSen = TextInput(password = True,size_hint=[.5,.4],pos_hint={'x' : .25})

        label_vazia = Label(text=' ',size_hint=[.4,.4]) #funciona mais e feio
        label_vazia2 = Label(text=' ',size_hint=[.4,.4]) #funciona mais e feio
        label_us = Label(text = 'Digite seu usuario',font_size=30,size_hint=[.4,.4],pos_hint={'x' : .25})
        label_sen = Label(text ='Digite a sua senha',font_size=30,size_hint=[.4,.4],pos_hint={'x' : .25})

        box.add_widget(label_us)
        box.add_widget(self.boxUser)
        box.add_widget(label_sen)
        box.add_widget(self.boxSen)
        box.add_widget(label_vazia)
        box.add_widget(botao)
        box.add_widget(label_vazia2)

        self.db.get_rows()
        return box

    def recebe(self,botao):
        self.db = DbCon()
        recUsuario = self.boxUser.text
        recSenha = self.boxSen.text

        self.db.c.execute("select count(*),id_usu from usuario where nome = '"+str(recUsuario)+"' and senha = '"+str(recSenha)+"'") #coloca recUsuario na instrucao do banco
        test = self.db.c.fetchone() #busca uma linha

        
        if(test['count(*)'] == 1):
            self.confirma_login()
            id_session = test['id_usu']
            print(id_session)
        else:
            self.login_errado()
        
        
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
        
    def get_rows(self):
        global users
        sql = "SELECT * FROM usuario"
        self.c.execute(sql)
        users = self.c.fetchall()
        
        for x in users:
            print(x)
        return self.c.fetchall()
    
Principal().run()
