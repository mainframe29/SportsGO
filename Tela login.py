from kivy.app import App

import pymysql

from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Principal(App):

    
    def build(self):
        self.db = DbCon()
        box = BoxLayout(orientation = 'vertical')
        botao = Button(text = 'Entrar',on_press = self.recebe)

        self.boxUser = TextInput()
        self.boxSen = TextInput(password = True)

        label_us = Label(text = 'Digite seu usuario')
        label_sen = Label(text ='Digite a sua senha')

        box.add_widget(label_us)
        box.add_widget(self.boxUser)
        box.add_widget(label_sen)
        box.add_widget(self.boxSen)
        box.add_widget(botao)

        self.db.get_rows()
        return box

    def recebe(self,botao):
        self.db = DbCon()
        recUsuario = self.boxUser.text
        recSenha = self.boxSen.text

        usuario = 'Karine' #banco de dados
        senha = '123' #banco de dados

        self.db.c.execute("select count(*) from usuario where nome = '"+str(recUsuario)+"' and senha = '"+str(recSenha)+"'") #coloca recUsuario na instrucao do banco
        test = self.db.c.fetchone() #busca uma linha

        
        if(test['count(*)'] == 1):
            print("Deu certo pohaaaaaaaaaaa, graças ao supremo senhor do universo")
        else:
            print('usuario ou senha incorreta')
        
        
##########################teste de conexao com banco de dados
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
