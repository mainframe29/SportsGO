import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse
import pymysql

id_session = 2

class Perfil(GridLayout):
    global id_session

    qtd = 0

    #puxaUsuario() #chama puxaUsuario

    def puxaUsuario(self):

        self.db = DbCon()
        nick = self.db.c.execute("SELECT nick FROM usuario WHERE id_usu = " + str(id_session)) #pega o nick
        n = self.db.c.fetchone() #coloca o comando num vetor
        self.lblTxt.text = n['nick']

        #self.puxaQtdPosts #chama puxaQtdPosts
        return self.lblTxt.text


    def puxaQtdPosts(self):
        qtd = self.db.c.execute("SELECT count(id_video) FROM videos WHERE id_usu = id_session") #pega a quantidade de videos

        self.exibe #chama exibe


    def exibe(self):
        i = 0
        posts = []
        while(i < qtd):
            titulo = self.db.c.execute("SELECT titulo FROM videos WHERE id_usu = id_session")
            lblPost.titPost.text = titulo

            img = self.db.c.execute("SELECT url FROM videos WHERE id_usu = id_session")
            lblPost.imgPost.source = img

            legenda = self.db.c.execute("SELECT legenda FROM videos WHERE id_usu = id_session")
            lblPost.legendaPost.text = legenda

            tag = self.db.c.execute("SELECT tag FROM videos WHERE id_usu = id_session")
            lblPost.tagPost.text = tag

            posts.append[(titulo, img, legenda, tag)]

            i += 1



class perfilApp(App):
    def build(self):
        return Perfil()


class DbCon:
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost',
                                  user = 'root',
                                  password = '',
                                  db = 'sports',
                                  charset = 'utf8mb4',
                                  cursorclass = pymysql.cursors.DictCursor)
        self.c = self.db.cursor()


if __name__ == '__main__':
    perfilApp().run() 