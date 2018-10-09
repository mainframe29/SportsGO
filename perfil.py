import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
import pymysql

id_session = 1
class DbCon:
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '',
                                  db = 'sports',
                                  charset = 'utf8mb4',
                                  cursorclass = pymysql.cursors.DictCursor)
        self.c = self.db.cursor()

class Perfil(BoxLayout):
    global id_session
    #puxaUsuario() #chama puxaUsuario

    def puxaUsuario(self):

        self.db = DbCon()
        self.db.c.execute("SELECT nome, nick, pontos FROM usuario WHERE id_usu = " + str(id_session)) #pega o nick
        self.n = self.db.c.fetchone() #coloca o comando num vetor

        #self.puxaQtdPosts #chama puxaQtdPosts
        return str(self.n['nome']+" @"+str(self.n['nick'])+"     Pontos: "+str(self.n['pontos']))


    def __init__(self,**kwargs):
        super(Perfil,self).__init__(**kwargs)
        global id_session
        self.db = DbCon()
        self.db.c.execute("select * from videos where id_usu = "+str(id_session))

        for row in self.db.c:
            self.linhas = BoxLayout(orientation = 'vertical')
            self.legenda = Label(text = row['legenda'], color = [0,0,0,1],size = self.size, pos = self.pos)
            self.linhas.add_widget(self.legenda)
            self.img = Image(source = row['url'],size = self.size, pos = self.pos)
            self.linhas.add_widget(self.img)
            self.fotos_bl.add_widget(self.linhas)
            self.fotos_bl.add_widget(Label(text = ''))

        #self.add_widget(self.Fotos)

        
class perfilApp(App):
    def build(self):
        return Perfil()





if __name__ == '__main__':
    perfilApp().run() 

'''while(i < qtd):
            titulo = self.db.c.execute("SELECT titulo FROM videos WHERE id_usu ="+str(id_session))
            lblPost.titPost.text = titulo

            img = self.db.c.execute("SELECT url FROM videos WHERE id_usu = "+str(id_session))
            lblPost.imgPost.source = img

            legenda = self.db.c.execute("SELECT legenda FROM videos WHERE id_usu = "+str(id_session))
            lblPost.legendaPost.text = legenda

            tag = self.db.c.execute("SELECT tag FROM videos WHERE id_usu = "+str(id_session))
            lblPost.tagPost.text = tag

            posts.append[(titulo, img, legenda, tag)]

            i += 1


'''