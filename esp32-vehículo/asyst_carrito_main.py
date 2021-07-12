#----------------------Librerías a utilizar-----------------------
from sys import settrace
from requests.api import post
from machine import Pin, PWM, ADC, time
import json 
import time
import .libs_asyst as lib
import requests
#-----------------------Pines a utilizar---------------------------
US_trigger_pin= 1
US_echo_pin   = 2
pin_boton_frenado = Pin(3, Pin.In)
pin_sensor_IFR    = [0,0,0,0,0] #4,5,6,7,8
pin_sensor_IFR[0] = Pin(4, Pin.IN)
pin_sensor_IFR[1] = Pin(5, Pin.IN)
pin_sensor_IFR[2] = Pin(6, Pin.IN)
pin_sensor_IFR[3] = Pin(7, Pin.IN)
pin_sensor_IFR[4] = Pin(8, Pin.IN)
pin_alarma_balanza= Pin(9, Pin.IN)
pin_sensor_MG     = Pin(10, Pin.IN)
pin_M_L_sentido   = Pin(11, Pin.OUT)
pin_M_L_pwm       = 12 #referencia visual solamente
pin_M_R_sentido   = Pin(13, Pin.OUT)
pin_M_R_pwm       = 14 #referencia visual solamente
pin_boton_fisico  = Pin(15, Pin.IN)

#----------------Variables y objetos a utilizar---------------------
class URL:
    def __init__(self):
        self.get ='http://127.0.0.1:8000/prueba_read.json'#Cambiar por la url y el nombre del archivo a buscar
        self.send = 'http://127.0.0.1:8000' 
        self.carrito_json = 'prueba_read.json'
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
freq_pwm = 10000
pin_M_L_pwm = PWM(Pin(12),freq_pwm)
pin_M_R_pwm = PWM(Pin(14),freq_pwm)
M_L_sentido,M_L_pwm,M_R_sentido,M_R_pwm = 0
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


#pines = [boton_frenado,sensor_IFR, alarma_balanza, sensor_MG]
#--------------------------------------------------------------
def main():
    while 1:
        while server_dict['destino'] == None:
            try: 
                server_dict = lib.get_from_server(server_dict)
                #destino = server_dict['destino']
            except: pass

        boton_frenado, sensor_IFR, alarma_balanza, sensor_MG,boton_fisico = lib.actualizar_valores(pin_boton_frenado,pin_sensor_IFR, pin_alarma_balanza, pin_sensor_MG)
        #if confirmacion == 0 and boton_fisico==1:
        #    confirmacion = 1
        if server_dict['entrega']==True and boton_fisico==1: comenzar = 1
        elif server_dict['entrega']==False: comenzar = 1
        else: comenzar = 0
        if comenzar:
            direccion = lib.corregir_rumbo(sensor_IFR)
            if sensor_MG:
                carrito_dict, direccion, countIman, server_dict,comenzar = lib.reconocimiento_sector(server_dict,countIman,destinoPanol,carrito_dict)
            interrupcion = lib.frenado_emergencia(boton_frenado,sensor_US)
            interrupcion += alarma_balanza 
            M_L_sentido,M_L_pwm,M_R_sentido,M_R_pwm = lib.regular_direccion(direccion,velocidades_dict)
            lib.regular_sentido_motores(pin_M_L_sentido,pin_M_R_sentido,M_L_sentido,M_R_sentido)
            lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,interrupcion,M_L_pwm,M_R_pwm)

            if direccion==8:
                carrito_dict['perdido'] = 1 #Pregunto si está perdido
                carrito_send_final = [carrito_dict]
                requests.post('http://127.0.0.1:8000', json=carrito_send_final)
            else: carrito_dict['perdido'] = 0

            

main()
#?NOTA DEL DÍA: Queda hacer que la variable "comenzar" vuelva a cero además de mandar los dict

#!Esperar y averiguar dónde es necesario un time.sleep()