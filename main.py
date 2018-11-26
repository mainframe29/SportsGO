import kivy
from kivy.app import App
from kivy.app import Widget
import cv2
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
import pymysql
from kivy.uix.image import Image
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

class Cadastro_ou_login(Screen):
    pass

class Perfil(Screen):
    global Id_Session
    def puxaUsuario(self):

        self.db = DbCon()
        nick = self.db.c.execute("SELECT nick FROM usuario WHERE id_usu = " + str(Id_Session)) #pega o nick
        n = self.db.c.fetchone() #coloca o comando num vetor
        self.lblTxt.text = n['nick']

        #self.puxaQtdPosts #chama puxaQtdPosts
        return self.lblTxt.text


    def __init__(self,**kwargs):
        super(Screen,self).__init__(**kwargs)
        global Id_Session
        self.tblImg = GridLayout(cols = 3, padding = [30, 0, 30, 30])
        if(Id_Session!= 0):
            self.db = DbCon()
            self.db.c.execute("select url, legenda from videos where id_usu = "+str(Id_Session))
           
            for row in self.db.c:
                self.linhas = BoxLayout(orientation = 'vertical')
                print('url: '+str(row))
                self.img = Image(source = row['url'], size = self.size, allow_stretch= True)
                self.linhas.add_widget(self.img)
                self.legenda = Label(text = row['legenda'], shorten= True, font_size = 15, size_hint_y= .3, size_hint_x= 1, text_size= [None, None], split_str= ' ', color= [0, 0, 0, 1])
                self.linhas.add_widget(self.legenda)
                self.tblImg.add_widget(self.linhas)
            self.add_widget(self.tblImg)   
        print('Passou aqui! '+str(Id_Session))
        
    pass

class TelaCadastro(Screen):
    def insert_user(self):
        self.db = DbCon()
        ''' no arquivo kv, eu coloquei o comando name_text_input : nome,
        ele apenas atribui o id do text input (nome) a essa variavel(name_text_input)
        '''
        self.nome = self.name_text_input.text
        self.user = self.usuario_text_input.text
        self.email = self.email_text_input.text
        self.senha = self.senha_text_input.text

        self.db.c.execute("select count(*)from usuario where nick like '"+self.user+"'")
        self.userExist = self.db.c.fetchone()#uso o um select count para contar quantos usuarios existem para o digitado
        self.db.c.execute("select count(*)from usuario where email like '"+self.email+"'")
        self.emailExist = self.db.c.fetchone()#uso o um select count para contar quantos email existem para o digitado

        if(self.userExist['count(*)'] == 0 and self.emailExist['count(*)'] == 0): #só da o insert se o o count dos dois for 0
            sql = "INSERT INTO usuario VALUES(0,'"+self.nome+"', '"+self.user+"', '"+self.email+"', '"+self.senha+"', 1, 0)"
            self.db.c.execute(sql)
            self.parent.current = 'login'
        else:
            print('usuario ou email invalido!')
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
            Id_Session = test['id_usu']
            print(str(Id_Session))
            PaginaInicial().informacao()
            self.confirma_login()
        else:
            self.login_errado()
    pass

class PaginaInicial(Screen):
    def informacao(self):
        global Id_Session
        self.db = DbCon()
        sql = "select nome from usuario where id_usu = %s"
        texto=self.db.c.execute(sql, Id_Session)
        texto = self.db.c.fetchone()
        self.infTxt.text = str(texto['nome'])
        print(self.infTxt.text)
    def validar(self):
        global Pergunta
        if(Pergunta!=0):
            layout      = GridLayout(cols=1, padding=10)
            popupLabel  = Label(text  = "Você ja completou o quiz diario, volte amanhã")
            closeButton = Button(text = "Ok")
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)   
            popup = Popup(title='Alerta!',
                              content=layout)
                #content=(Label(text='This is a demo pop-up')))
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
            self.parent.current = 'paginaInicial'
    pass
 
class LabelConfig(Screen):
    def __init__(self,**kwargs):
        super(Screen,self).__init__(**kwargs)
        global Id_Session, Pergunta
        if(Pergunta==0):
            self.orientation = "horizontal"

            self.questao_field = BoxLayout(orientation="horizontal")
            #self.table = GridLayout(cols=5,rows=2)
            self.db = DbCon()
            self.table = BoxLayout(orientation = "vertical")
            
            
            self.rows = [[Label(text ='pergunta', color = [0,0,0,1], text_size= (self.center_x*5,None)),Button(text="Alternativa A"),
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
                layout      = GridLayout(cols=1, padding=10)
                popupLabel  = Label(text  = "O Quiz chegou ao fim, aguarde até amanhã para poder fazer novamente :)")
                closeButton = Button(text = "Finalizar")
                layout.add_widget(popupLabel)
                layout.add_widget(closeButton)   
                popup = Popup(title='Alerta!',
                              content=layout)
                #content=(Label(text='This is a demo pop-up')))
                popup.open()
                closeButton.bind(on_press=popup.dismiss)
                self.parent.current = 'paginaInicial'

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


class Tela(Screen):
    def hist_plus_rules(self):
        hist=str(self.get_history())+'\n'+str(self.get_rules())
        return hist
        
    def get_history(self):
        self.db = DbCon()

        texto=self.db.c.execute("select historia from esportes")
        texto = self.db.c.fetchone()

        return str(texto['historia'])

    def get_name(self):
        self.db = DbCon()
        texto = self.db.c.execute("select nome from esportes")
        texto = self.db.c.fetchone()

        return str(texto['nome'])
    def get_rules(self):
        self.db = DbCon()
        texto = self.db.c.execute("select regras from esportes")
        texto = self.db.c.fetchone()

        return str(texto['regras'])
    pass

class ScreenManagement(ScreenManager):
    def switch_to_Cadastra(self):
        self.current = 'telaCadastro'

    def switch_to_Perfil(self):
        self.current = 'perfil'
        
    def switch_to_labelConfig(self):
        self.current = 'labelConfig'
         
    def switch_to_paginaInicial(self):
        self.current = 'paginaInicial'
        
    def switch_to_Login(self):
        self.current = 'login'

    def switch_to_missoes(self):
        self.current = 'missoes'
        
    def switch_to_esporteDia(self):
        self.current = 'esporteDia'

class kivyWizardApp(App):
    def build(self):
        self.root = ScreenManagement()
        return self.root
 
if __name__ == '__main__':
    kivyWizardApp().run()