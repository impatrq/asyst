#----------------------Librerías a utilizar-----------------------
from machine import Pin, PWM
import time
import ujson 
import urequests
import time
import lib_asyst as lib

sta_if = network.WLAN(network.STA_IF);    # instancia el objeto -sta_if- para controlar la interfaz STA
sta_if.active(True)                       # activa la interfaz STA del ESP32
sta_if.disconnect()
if sta_if.isconnected(): sta_if.disconnect()
print(sta_if.scan())
sta_if.connect("Avionica 2B","Atlantida2020")    # inicia la conexión con el AP
while not sta_if.isconnected():
    time.sleep(0.5)
print("conectado:", sta_if.isconnected())

#-----------------------Pines a utilizar---------------------------
#No se pueden usar: 6 al 11, 20, 23, 24, 28 a 31, 37, 38 

pin_sensor_IFR    = [0,0,0] #4,5,12,13,14
pin_sensor_IFR[0] = Pin(34, Pin.IN)
pin_sensor_IFR[1] = Pin(35, Pin.IN)
pin_sensor_IFR[2] = Pin(32, Pin.IN)
#pin_sensor_IFR[3] = Pin(33, Pin.IN)

freq_pwm = 300
pin_M_L_forw      = Pin(27, Pin.OUT)
pin_M_L_back      = Pin(14, Pin.OUT)
pin_M_R_forw      = Pin(12, Pin.OUT)
pin_M_R_back      = Pin(13, Pin.OUT)
pin_M_L_pwm       = PWM(Pin(26),freq_pwm)
pin_M_R_pwm       = PWM(Pin(25),freq_pwm)
pin_confirmacion  = Pin(18, Pin.IN, Pin.PULL_DOWN)

pin_sensor_MG     = Pin(21, Pin.IN)
pin_sensor_MG_2   = Pin(4, Pin.IN)

#US_trigger_pin    = 0
#US_echo_pin       = 15
#sensor_US = lib.HCSR04 (US_trigger_pin, US_echo_pin)


#----------------Variables y objetos a utilizar---------------------

URL = lib.URLs('http://192.168.0.4:8000/carrito/?matricula=420','http://192.168.0.4:8000/carrito/?matricula=420',420)#ipGet, ipPost, matricula
direccion = 0
destino = []   #Próximamente se le preguntará al servidor el destino
countIman = 0
delay = 0
M_L_forw=0
M_L_back=0
M_L_pwm=0
M_R_forw=0
M_R_back=0
M_R_pwm=0
#confirmacion = 0
start = 0
sensor_IFR=[0,0,0]
interrupcion = 0
delay = False
esperandoMG2 = False


#pines = [boton_frenado,sensor_IFR, alarma_balanza, sensor_MG]
#--------------------------------------------------------------

while 1:
    #print("final de recorrido")#!-----------------
    print(pin_confirmacion.value())
    time.sleep(0.1)
    #lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,1,M_L_pwm,M_R_pwm)#*para asegurarnos que empiece frenado
    while pin_confirmacion.value()==0 and start==0:
        #print("valor:",pin_confirmacion.value())#!---------------------------
        time.sleep(0.1)
        if pin_confirmacion.value()==1:#todo: añadir Try para ver si recibe algo
            posicion_actual = []
            destinoPanol    = []#La cantidad de ceros depende del circuito
            destino = URL.get_from_server()
            for i in destino:
                posicion_actual.append(0)
                destinoPanol.append(0)
            #print(destino)#!------------------------------------------
            start = 1
            #print("EMPEZAMOS UN RECORRIDO")#!-------------------------------------------
            break
    
    while start:
        sensor_IFR, sensor_MG, sensor_MG_2 = lib.actualizar_valores(pin_sensor_IFR, pin_sensor_MG, pin_sensor_MG_2)
        
        direccion = lib.corregir_rumbo(sensor_IFR)
        
        if sensor_MG: 
            #esperandoMG2=True
        #if sensor_MG_2 and esperandoMG2:
            #esperandoMG2 = False
            destino, direccion, countIman, posicion_actual, delay,start= lib.reconocimiento_sector(destino,countIman,destinoPanol,posicion_actual,URL)
            print(destino, posicion_actual)
        if esperandoMG2: direccion = 3
        #interrupcion = lib.frenado(sensor_US)
        M_L_forw,M_L_back, M_L_pwm,M_R_forw,M_R_back, M_R_pwm = lib.regular_direccion(direccion)
        lib.regular_sentido_motores(pin_M_L_forw,pin_M_L_back,M_L_forw,M_L_back,  pin_M_R_forw,pin_M_L_back,M_R_forw,M_R_back)

        if direccion==6:#* SE MANTIENE FRENADO HASTA QUE SE PULSA EL BOTÓN DE CONFIRMACIÓN FÍSICA
            lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,1,M_L_pwm,M_R_pwm)
            #print("esperando botón de confirmación")#!---------------------------
            while not pin_confirmacion.value():pass
            #print("REGRESANDO...")#!----------------
            time.sleep(3) #tiempo de espera para no atropellar a nadie

        lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,interrupcion,M_L_pwm,M_R_pwm)

        if not interrupcion:#* EL PROGRAMA SE PAUSA HASTA TERMINAR DE COMPLETAR LOS GIROS A 90° O 180°
            if delay and direccion==6:
                time.sleep(2) #cambiar por el tiempo que corresponde
                delay = False
            elif delay: 
                time.sleep(1)#cambiar por el tiempo que corresponde
                delay = False      
        #terminar de hacer xd
        #if direccion==8:    


