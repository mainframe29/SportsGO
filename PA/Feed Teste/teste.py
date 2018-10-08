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
    Builder.load_file('TelaFeed.kv')
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.bl = BoxLayout(orientation = 'vertical')
        self.db = DbCon()
        self.db.c.execute("select * from videos")
        self.post = self.db.c.fetchall()
        self.rows = Label(text= 'oi')
        
        '''for i in self.rows:
            self.bl.add_widget(i)
        for row in enumerate(self.post):
            self.img = Image(source = row['url'])
            self.bl.add_widget(self.img)'''
        self.add_widget(self.bl)

        

class SportsGo(App):
    def build(self):
        return Feed()

SportsGo().run()
