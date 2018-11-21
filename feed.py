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

class Feed(BoxLayout):
    Builder.load_file('feed.kv')
    global id_session
    

    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        global id_session
        self.bl.add_widget(Label(text= "Posts: \n", pos = self.pos, size = self.size))
        self.db = DbCon()
        self.db.c.execute("select id_usu from usuario inner join seguir on usuario.id_usu = seguir.id_seguidor where seguir.id_seguindo=" + str(id_session))
        self.n = self.db.c.fetchall()
        for i in self.n:
            print(str(i) + 'AA')
            self.db.c.execute("select us.nome, vi.legenda, vi.url, vi.tag, es.nome from usuario us inner join videos vi on us.id_usu=vi.id_usu inner join esportes es on vi.tag= es.id_spo where us.id_usu = " + str(i['id_usu']))
            
            self.f = self.db.c.fetchall()
            for row in self.f:
                print(row)
                self.bl.add_widget(Label(text = str(row['nome'])+": "+str(row['legenda'])+"\n", color = [0,0,0,1],pos = self.pos, size = self.size))
                self.bl.add_widget(Image(source = str(row['url']), pos = self.pos, size = [500,500]))
                self.bl.add_widget(Label(text = str(row['es.nome'])+"\n", pos = self.pos, size = self.size, color = [0,0,0,1]))
                
        
        
    pass
class SportsGo(App):
    def build(self):
        return Feed()

SportsGo().run()