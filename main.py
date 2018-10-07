import kivy
from kivy.app import App
from kivy.app import Widget
import cv2
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import pymysql

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
kivy.require('1.8.0')
 
__version__ = "0.1"

Pergunta = 0
Id_Session = 1
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

 
class PaginaInicial(Screen):
    pass

class Login(Screen):        
    def confirma_login(self):
        b = BoxLayout(orientation='vertical')
        voltar = Button(text='Voltar')
        aviso = Label(text='Login finalizado com sucesso')
        
        b.add_widget(aviso)
        b.add_widget(voltar)
        pop = Popup(title='Login',content=b)
        pop.open()
        voltar.bind(on_press = pop.dismiss)
        self.parent.current = 'paginaInicial' #chama tela q esta no .kv

    def login_errado(self):
        b = BoxLayout(orientation='vertical')
        
        voltar = Button(text='Voltar')
        aviso = Label(text='Usuario ou senha incorretos!!!')

        b.add_widget(aviso)
        b.add_widget(voltar)

        pop=Popup(title='Login',content=b)
        pop.open()
        voltar.bind(on_press=pop.dismiss)
        #self.db.get_rows()

    def recebe(self):
        global Id_Session
        self.db = DbCon()
        recUsuario = self.usuTxt.text
        recSenha = self.senhTxt.text

        self.db.c.execute("select count(*),id_usu from usuario where nick = '"+str(recUsuario)+"' and senha = '"+str(recSenha)+"'") #coloca recUsuario na instrucao do banco
        test = self.db.c.fetchone() #busca uma linha

        
        if(test['count(*)'] == 1):
            self.confirma_login()
            Id_Session = test['id_usu']
            print(Id_Session)
        else:
            self.login_errado()
    pass
 
class LabelConfig(Screen):
    def __init__(self,**kwargs):
        super(Screen,self).__init__(**kwargs)
        global Id_Session
        self.orientation = "horizontal"

        self.questao_field = BoxLayout(orientation="horizontal")
        #self.table = GridLayout(cols=5,rows=2)
        self.db = DbCon()
        self.table = BoxLayout(orientation = "vertical")
        
        
        self.rows = [[Label(text ='pergunta'),Button(text="Alternativa A"),
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
        global Pergunta, Id_Session
        print(Id_Session)
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
                sql = "update usuario set pontos = pontos + 1 where id_usu = "+str(Id_Session)
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
    pass
class Missoes(Screen):
    global Id_Session
    def recebe(self):
        self.db = DbCon()
        self.rec_legenda = self.legenda_text_input.text
        self.db.c.execute("select nick from usuario where id_usu = "+str(Id_Session))
        self.nome_usu = self.db.c.fetchone()
        self.num = 0
        self.db.c.execute("select count(*) from videos where url = '"+(str(self.nome_usu['nick']) + '_img'+str(self.num)+'.png')+"'")
        self.cont = self.db.c.fetchone()
        while(self.cont['count(*)'] != 0):
            self.db.c.execute("select count(*) from videos where url = '"+(str(self.nome_usu['nick']) + '_img'+str(self.num)+'.png')+"'")
            self.cont = self.db.c.fetchone()
            if(self.cont['count(*)']!=0):
                self.num= self.num+1
        self.rec_url = (str(self.nome_usu['nick']) +'_img'+str(self.num)+'.png')
        self.foto(self.rec_url)
        self.db.c.execute("INSERT INTO videos VALUES (0, 'titulo', '"+str(self.rec_url)+"', '"+self.rec_legenda+"', "+str(Id_Session)+", 1)")
        self.db.c.execute("select tag from videos where id_usu= "+str(Id_Session)+" order by id_video desc limit 1")
        self.tag = self.db.c.fetchone()
        if(self.tag['tag'] == 1):
            self.db.c.execute("update usuario set pontos = pontos + 10 where id_usu ="+str(Id_Session))
    def foto(self,rec_url):
        
        camera_port = 0
      
        nFrames = 30
      
        camera = cv2.VideoCapture(camera_port)
         
        file = rec_url
             
        print ("Digite <ESC> para sair / <s> para Salvar" )  
         
        emLoop= True
          
        while(emLoop):
         
            retval, img = camera.read()
            cv2.imshow('Foto',img)
         
            k = cv2.waitKey(100)
         
            if k == 27:
                emLoop= False
             
            elif k == ord('s'):
                cv2.imwrite(file,img)
                emLoop= False
         
        cv2.destroyAllWindows()
        camera.release()
        return
    pass

class ScreenManagement(ScreenManager):
    def switch_to_labelConfig(self):
        self.current = 'labelConfig'
         
    def switch_to_paginaInicial(self):
        self.current = 'paginaInicial'
        
    def switch_to_Login(self):
        self.current = 'login'

    def switch_to_missoes(self):
        self.current = 'missoes'

class kivyWizardApp(App):
    def build(self):
        self.root = ScreenManagement()
        return self.root
 
if __name__ == '__main__':
    kivyWizardApp().run()