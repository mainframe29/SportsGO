from kivy.app import App

import pymysql

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

Pergunta = 0

class DbCon:
    
    
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='',
                                  db='sports',
                                  charset = 'utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        self.c = self.db.cursor()


    def get_rows(self):    
        global Pergunta
        sql = "SELECT * FROM quiz WHERE esporte = 1 limit %s,1"
        self.c.execute(sql, Pergunta)
        return self.c.fetchall()

class Table(BoxLayout):

    def __init__(self,**kwargs):
        super(Table,self).__init__(**kwargs)

        self.orientation = "horizontal"

        self.questao_field = BoxLayout(orientation="horizontal")
        #self.table = GridLayout(cols=5,rows=2)
        self.db = DbCon()
        self.table = BoxLayout(orientation = "vertical")
        self.rows = [[Label(text="pergunta"),Button(text="Alternativa A"),
                      Button(text="Alternativa B"), Button(text="Alternativa C"),
                      Button(text="Alternativa D"),]]

        for pergunta, alternativaA, alternativaB, alternativaC, alternativaD in self.rows:
            self.table.add_widget(pergunta)
            self.table.add_widget(alternativaA)
            self.table.add_widget(alternativaB)
            self.table.add_widget(alternativaC)
            self.table.add_widget(alternativaD)

        self.add_widget(self.table)


        self.db = DbCon()
        self.update_table()
        
    def update_table(self):
        db = DbCon()
        self.db.c.execute("select count(*) from quiz where esporte = 1")
        for row in self.db.c:
            if(row['count(*)'] > Pergunta):
                for index,row in enumerate(self.db.get_rows()):
                    self.rows[index][0].text = str(row['pergunta'])
                    self.rows[index][1].text = str(row['alternativaA'])
                    self.rows[index][1].bind(on_press=self.change_question)
                    self.rows[index][2].text = str(row['alternativaB'])
                    self.rows[index][2].bind(on_press=self.change_question)
                    self.rows[index][3].text = str(row['alternativaC'])
                    self.rows[index][3].bind(on_press=self.change_question)
                    self.rows[index][4].text = str(row['alternativaD'])
                    self.rows[index][4].bind(on_press=self.change_question)
            else:
                self.clear_table()

    def clear_table(self):
        for index in range(1):
            self.rows[index][0].text = ""
            self.rows[index][1].text = ""
            self.rows[index][2].text = ""
            self.rows[index][3].text = ""
            self.rows[index][4].text = ""


    def search(self, *args):
        self.clear_table()
        self.update_table(self.search_input.text)

    def change_question(self, botao):
        global Pergunta
        db=DbCon()
        for index, row in enumerate(db.get_rows()):
            if(str(row['resposta']) == str(botao.text[0])):
                layout      = GridLayout(cols=1, padding=10)
                popupLabel  = Label(text  = "Resposta Certa!")
                closeButton = Button(text = "OK!")
                layout.add_widget(popupLabel)
                layout.add_widget(closeButton)   
                popup = Popup(title='Alerta!',
                              content=layout)
                #content=(Label(text='This is a demo pop-up')))
                popup.open()
                closeButton.bind(on_press=popup.dismiss)

                sql = "update usuario set pontos = pontos + 1 where id_usu = 1"
                db.c.execute(sql)
            else:
                layout      = GridLayout(cols=1, padding=10)
                popupLabel  = Label(text  = "Resposta Errada!")
                closeButton = Button(text = "OK!")
                layout.add_widget(popupLabel)
                layout.add_widget(closeButton)   
                popup = Popup(title='Alerta!',
                              content=layout)
                #content=(Label(text='This is a demo pop-up')))
                popup.open()
                closeButton.bind(on_press=popup.dismiss)
        Pergunta += 1
        self.update_table()



class MyApp(App):
    def build(self):
        return Table()


MyApp().run()
