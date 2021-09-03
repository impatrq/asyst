#----------------------Librerías a utilizar-----------------------
from sys import settrace
from requests.api import post
from machine import Pin, PWM, ADC, time
import json 
import time
import .libs_asyst as lib
import requests

#-----------------------Pines a utilizar---------------------------
#No se pueden usar: 6 al 11, 20, 23, 24, 28 a 31, 37, 38 
US_trigger_pin= 1
US_echo_pin   = 2
pin_boton_frenado = Pin(3, Pin.IN)
pin_sensor_IFR    = [0,0,0,0,0] #4,5,12,13,14
pin_sensor_IFR[0] = Pin(4, Pin.IN)
pin_sensor_IFR[1] = Pin(5, Pin.IN)
pin_sensor_IFR[2] = Pin(12, Pin.IN)
pin_sensor_IFR[3] = Pin(13, Pin.IN)
pin_sensor_IFR[4] = Pin(14, Pin.IN)
pin_alarma_balanza= Pin(15, Pin.IN)
pin_sensor_MG     = Pin(16, Pin.IN)
pin_sensor_MG_2   = Pin(17, Pin.IN)
pin_M_L_forw      = Pin(18, Pin.OUT)
pin_M_L_back      = Pin(19, Pin.OUT)
#pin_M_L_pwm       = 21 #referencia visual solamente
pin_M_R_forw      = Pin(22, Pin.OUT)
pin_M_R_back      = Pin(25, Pin.OUT)
#pin_M_R_pwm       = 26 #referencia visual solamente
pin_M_enabled     = Pin(27, Pin.OUT)
pin_boton_confirm = Pin(32, Pin.IN)


#----------------Variables y objetos a utilizar---------------------
class URLs:
    def __init__(self):
        self.get ='http://127.0.0.1:8000/prueba_read.json'#Cambiar por la url y el nombre del archivo a buscar
        self.send = 'http://127.0.0.1:8000' 
        self.carrito_json = 'prueba_read.json'
URL = URLs()
direccion = 0
destino = []   #Próximamente se le preguntará al servidor el destino
countIman = 0
posicion_actual = []
destinoPanol = [0,0,0,0,0]#La cantidad de ceros depende del circuito
destino_anterior = []
server_dict = {
    'destino':None,
    'entrega':None
}
carrito_dict = {
    'posicion_actual':[0,0,0],
    'perdido':None
}
freq_pwm = 300
pin_M_L_pwm = PWM(Pin(21),freq_pwm)
pin_M_R_pwm = PWM(Pin(26),freq_pwm)
M_L_forw,M_L_back,M_L_pwm,  M_R_forw,M_R_back,M_R_pwm,boton_confirm = 0
sensor_US = lib.HCSR04 (US_trigger_pin, US_echo_pin)
velocidad = 65000
sensor_IFR=[0,0,0,0,0]
velocidades_dict={
    'p25' : int(velocidad/4),
    'p30' : int(velocidad/100)*30,
    'p40' : int(velocidad/100)*40,
    'p50' : int(velocidad/2),
    'p60' : int(velocidad/100)*60,
    'p75' : int(velocidad/4)*3,
    'p80' : int(velocidad/100)*80,
    'p90' : int(velocidad/100)*90,
    'p100' : velocidad
}
interrupcion = 0
confirmacion = 0
comenzar = 0
delay = False


#pines = [boton_frenado,sensor_IFR, alarma_balanza, sensor_MG]
#--------------------------------------------------------------
def main():
    while 1:
        #añadir función de recibir el json del server ACÁ
        while server_dict['destino'] == None:
            try:server_dict=lib.get_from_server(server_dict)
            except: pass

        boton_frenado, sensor_IFR, alarma_balanza, sensor_MG, sensor_MG_2 = lib.actualizar_valores(pin_boton_frenado,pin_sensor_IFR, pin_alarma_balanza, pin_sensor_MG)
        direccion = lib.corregir_rumbo(sensor_IFR)
        if sensor_MG: 
            esperandoMG2=True
        if sensor_MG_2 and esperandoMG2:
            esperandoMG2 = False
            carrito_dict, direccion, countIman, server_dict, delay= lib.reconocimiento_sector(destino,countIman,destinoPanol,server_dict)
        if esperandoMG2: direccion = 3
        interrupcion = lib.frenado_emergencia(boton_frenado,sensor_US)
        interrupcion += alarma_balanza
        M_L_forw,M_L_back, M_L_pwm,M_R_forw,M_R_back, M_R_pwm = lib.regular_direccion(direccion,velocidades_dict)
        lib.regular_sentido_motores(pin_M_L_forw,pin_M_L_back,M_L_forw,M_L_back,  pin_M_R_forw,pin_M_L_back,M_R_forw,M_R_back)

        if direccion==6:#* SE MANTIENE FRENADO HASTA QUE SE PULSA EL BOTÓN DE CONFIRMACIÓN FÍSICA
            lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,1,M_L_pwm,M_R_pwm)
            while not boton_confirm:
                boton_confirm = pin_boton_confirm.value()
            boton_confirm=0
            time.sleep(3)

        lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,interrupcion,M_L_pwm,M_R_pwm)

        if not interrupcion:#* EL PROGRAMA SE PAUSA HASTA TERMINAR DE COMPLETAR LOS GIROS A 90° O 180°
            if delay and direccion==6:
                time.sleep(2)
                delay = False
            elif delay: 
                time.sleep(1)
                delay = False      
        if direccion==8:
            carrito_dict['perdido'] = 1 #Pregunto si está perdido
            carrito_send_final = [carrito_dict]
            requests.post('http://127.0.0.1:8000', json=carrito_send_final)
        else: carrito_dict['perdido'] = 0



        

main()
