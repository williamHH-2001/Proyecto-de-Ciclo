from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
#Para el Banner
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.graphics import Color,RoundedRectangle
from functools import partial

#from conexion_BD import Conexion_BD
from pymongo import MongoClient

class Banner(FloatLayout):
    
    def __init__(self,fecha,hora,pulso,temperatura,oxigeno, **kwargs):
        self.fecha=str(fecha)
        self.hora=str(hora)
        self.pulso=str(pulso)
        self.temperatura=str(temperatura)
        self.oxigeno=str(oxigeno)
        super().__init__()
        with self.canvas.before:
            Color(rgba=(0,.5,1,.1))
            self.rect=RoundedRectangle(radius=[(15.0,15.0),(15.0,15.0),(15.0,15.0),(15.0,15.0)])
        
        self.bind(pos=self.update_rect,size=self.update_rect)

        #etiquetas
        self.title_fecha=MDLabel(text=self.hora,pos_hint={'center_x': .3, 'center_y':.5},size_hint=(.2,.3),halign='center')
        self.title_hora=MDLabel(text=self.fecha,pos_hint={'center_x': .1, 'center_y':.5},size_hint=(.2,.3),halign='left')
        self.title_pulso=MDLabel(text=self.pulso,pos_hint={'center_x': .5, 'center_y':.5},size_hint=(.2,.3),halign='left')
        self.title_temperatura=MDLabel(text=self.temperatura,pos_hint={'center_x': .7, 'center_y':.5},size_hint=(.2,.3),halign='left')
        self.title_oxigeno=MDLabel(text=self.oxigeno,pos_hint={'center_x': .9, 'center_y':.5},size_hint=(.2,.3),halign='left')

        #agregar widget
        self.add_widget(self.title_fecha)
        self.add_widget(self.title_hora)
        self.add_widget(self.title_pulso)
        self.add_widget(self.title_temperatura)
        self.add_widget(self.title_oxigeno)
        
        
    
    def update_rect(self,*args):
        self.rect.pos=self.pos
        self.rect.size=self.size
        

kv="""
<HistorialScreen>:
    name:'historial_screen'
    BoxLayout:
        
        id:Box_historial
        orientation: 'vertical'
        height: self.minimum_height
        padding:"30dp","15dp","30dp","30dp"

        canvas:
            Color: 
                rgba: 1,1,1,1
            Rectangle:
                pos:self.pos
                size:self.size
                    

        MDLabel:
            halign:'center'
            text:'Datos enviados agdg ad ada dsgsg  dsg d gs g  fdf'
            color_text: 0,0,0,0
            #font_style:'H2'
            size_hint: (1,.15)
        
        ScrollView:
            id:Scroll
            GridLayout:
                id:grid_banner
                cols:1
                padding:[20,20,20,20]
                size_hint_y:None
                height:self.minimum_height
                row_default_height:50
                padding:'10dp'
                spacing:'10dp'


"""

class HistorialScreen(MDScreen):
    Builder.load_string(kv)
    
    def __init__(self,**kw):
        super().__init__(**kw)
        self.ga='ga'
        
    
    def on_pre_enter(self):
        f=open('info_paciente.txt','r')
        linea_texto=f.readlines()
        f.close()
        dni=int(linea_texto[2])
        self.grid=self.ids['grid_banner']
        #obteniendo la lista
        client = MongoClient("mongodb+srv://WilliamHuaman:MUfbSr5qOCkXJWur@proyectoprogramacion.u4hsj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db=client.ProyectoProgramacion
        mediciones=db.mediciones_pacientes.find({'dni':dni},{'_id':0,'fecha':1,'hora':1,'pulso':1,'temperatura':1,'oxigeno':1}).sort('fecha_int',1)
        self.lista_mediciones=list(mediciones)

        
        for i in self.lista_mediciones:
            self.banner=Banner(i['fecha'],i['hora'],i['pulso'],i['temperatura'],i['oxigeno']) #,on_release=partial(self.borrar_banner,i[0],i[1])
            self.grid.add_widget(self.banner)
            #print(i['fecha'],i['hora'])
