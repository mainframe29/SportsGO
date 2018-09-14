from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class Principal(App):
    def build(self):
        box = BoxLayout(orientation = 'vertical')

        botao = Button(text = 'Entrar',on_press = self.recebe)

        self.boxUser = TextInput()
        self.boxSen = TextInput()

        label_us = Label(text = 'Digite seu usuario')
        label_sen = Label(text ='Digite a sua senha')

        box.add_widget(label_us)
        box.add_widget(self.boxUser)
        box.add_widget(label_sen)
        box.add_widget(self.boxSen)
        box.add_widget(botao)

        return box

    def recebe(self,botao):
        recUsuario = self.boxUser.text
        recSenha = self.boxSen.text

        usuario = 'Karine' #banco de dados
        senha = '123' #banco de dados

        
        if(str(recUsuario) == str(usuario) and str(recSenha) == str(senha)):
            print("deu certo")
        else:
            print('usuario ou senha incorreta')
        print(recUsuario,recSenha)
        
        
        
Principal().run()
        
