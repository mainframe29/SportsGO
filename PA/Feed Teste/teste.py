import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import pymysql

id_session = 2

class DbCon:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='',
                                  db='sports',
                                  charset = 'utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        self.c = self.db.cursor()

class Feed(GridLayout):

    global id_session
    Builder.load_file('TelaFeed.kv')

    def __init__(self, **kwargs):
        super(GridLayout, self).__init__(**kwargs)
        global id_session
        self.post_user = GridLayout(rows = 1)
        self.post_img = GridLayout(rows = 1)
        self.post_leg = GridLayout(rows = 1)
        self.post = GridLayout(rows = 1)
        self.db = DbCon()
        self.db.c.execute("select id_usu from usuario inner join seguir "
        +"on usuario.id_usu = seguir.id_seguidor where seguir.id_seguindo=" + str(id_session))
        self.n = self.db.c.fetchall()
        for i in self.n:
            print(str(i) + 'AA')
            self.db.c.execute("select * from videos where id_usu=" + str(i['id_usu']))
            self.f = self.db.c.fetchall()

            for row in self.f:
                print(str(row) + 'BB')
                self.usuario = Label(text = str(row['id_usu']), color = (0,0,0,1))
                self.post_user.add_widget(self.usuario)
                self.img = Image(source = row['url'], size = self.size)
                self.post_img.add_widget(self.img)
                self.legenda = Label(text = row['legenda'], color = (0,0,0,1), size = self.size)
                self.post_leg.add_widget(self.legenda)
                self.post.add_widget(self.post_user)
                self.post.add_widget(self.post_img)
                self.post.add_widget(self.post_leg)
        self.add_widget(self.post)

class SportsGo(App):
    def build(self):
        return Feed()

SportsGo().run()
