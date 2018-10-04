from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

import cv2
import time
import pymysql

class Tela(BoxLayout):
    Builder.load_file('missoes_graphics.kv')

    def recebe(self):
        self.rec_legenda = self.legenda_text_input.text
        self.rec_legenda = (self.rec_legenda + '.png')
        self.foto(self.rec_legenda)
        
    def foto(self,rec_legenda):
        
        camera_port = 0
      
        nFrames = 30
      
        camera = cv2.VideoCapture(camera_port)
         
        file = rec_legenda
             
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
    
class Principal(App):
    def build(self):

        return Tela()
        
Principal().run()
