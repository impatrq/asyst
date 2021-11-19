import time
from machine import Pin
import machine
import network
import urequests
import ujson

"""
1-gira mucho a la izquierda
2-gira un poco a la izqueirda
3-sigue recto
4-gira un poco a la derecha
5-gira mucho a la derecha
7-gira 90° a la izquierda
9-gira 90° a la derecha
8-PERDIDO
"""

class URLs:
    def __init__(self,ipGet,ipPost,matricula):
        self.get  = ipGet#Cambiar por la url y el nombre del archivo a buscar
        self.post = ipPost
        self.matricula = matricula
    
    def get_from_server(self):
        '''Obtiene un nuevo destino del servidor'''
        #matricula, rumbo, ocupado, viajando, idavuelta, perdido
        resp = urequests.get(self.get).content
        resp=resp.decode("utf-8")
        #print(resp)
        server_dict = ujson.loads(resp)
        destino = server_dict['rumbo'].split(",")
        for i in range(len(destino)):
            destino[i] = int(destino[i])
        return destino
    
    def send_to_server(self,data:dict):
        '''Envía la información ingresada al servidor'''
        #nombres = ['ocupado', 'viajando', 'idavuelta','perdido','pos_actual','reset']
        for i in data:
            key = i
        data = str(self.matricula) + '-' + str(key) + '-' + str(data[key])
        resp = urequests.post(self.post, data=data)
        resp.close()

def actualizar_valores(pin_sensor_IFR=0, pin_sensor_MG=0,pin_sensor_MG_2=0,pin_confirmacion=0):#todo:usado
    '''Actualiza los valores de los sensores IFR, la alarma de balanza y sensores magnéticos'''
    sensor_IFR = [0,0,0,0]
    for i in range (4):
        sensor_IFR[i] = pin_sensor_IFR[i].value()
    sensor_MG = pin_sensor_MG.value()
    sensor_MG_2 = pin_sensor_MG_2.value()
    return sensor_IFR, sensor_MG, sensor_MG_2

def corregir_rumbo(aux):#todo: usado  #ingresa una lista con los valores 1/0 de los sensores Infrarrojos.
    '''Devuelve una dirección en base a los sensores IFR'''
    if   aux==[0,0,0,1]: return 5; #gira mucho a la derecha
    elif aux==[0,0,1,1]: return 4; #gira un poco a la derecha
    elif aux==[0,1,1,1]: return 4; #gira un poco a la derecha
    elif aux==[0,1,1,0]: return 3; #linea recta
    elif aux==[1,1,1,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,1,0,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,0,0,0]: return 1; #gira un poco a la izquierda
    else: return 8; #Perdido D:

def frenado(sensor_US):
    distancia = sensor_US.distance_cm() #Recordar crear el objeto de sensor_US
    if distancia>=100: return 0;
    else: return 1;



class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.

    The timeouts received listening to echo pin are converted to OSError('Out of range')

    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms
    
def reconocimiento_sector(destino, countIman, destinoPanol,posicion_actual, URL):#todo:usado

    if destino == destinoPanol:
        countIman -= 1
        posicion_actual[0] = countIman
         
        if (countIman > destino[0]) and (posicion_actual != destino):
            if      posicion_actual[countIman] == 7: auxDireccion = 9
            elif    posicion_actual[countIman] == 9: auxDireccion = 7
            else:   auxDireccion = 3
            posicion_actual[countIman] = 0
            if auxDireccion==9 or auxDireccion==7: delay = True
            else: delay=False
            return destino, auxDireccion, countIman,posicion_actual, delay,1
        elif posicion_actual == destino: 
            #print("Llegamos al Pañol")#!----------------
            destino = None #Reseteo La variable de destino para esperar uno nuevo
            URL.send_to_server({'reset':True})
            return destino, 6, countIman, posicion_actual,False,0

    else:
        countIman += 1
        posicion_actual[0] = countIman
        if (countIman < destino[0]) and (posicion_actual != destino):  
            posicion_actual[countIman] = destino[countIman]
            auxDireccion = int(posicion_actual[countIman])
            if auxDireccion==9 or auxDireccion==7: delay = True
            else: delay=False
            return destino, auxDireccion, countIman, posicion_actual,delay,1
        else: 
            #print("Llegamos a Destino")#!----------------
            destino = destinoPanol
            URL.send_to_server({'viajando':False})
            URL.send_to_server({'idavuelta':True})
            return destino, 6, countIman, posicion_actual,False,1
            
def regular_direccion(direccion): #todo:usado            #Recordar importar las los valores de "p" como un diccionario
    '''Devuelve una configuración para las ruedas en base a la dirección y los porcentajes de potencia ingresados'''    
    p1 = 150
    p2 = 200
    p3 = 250
    p4 = 300
    p5 = 300
    if      direccion == 1: return  1,0,p1-70, 1,0,p3 
    elif    direccion == 2: return  1,0,p2-80, 1,0,p3
    elif    direccion == 3: return  1,0,p4-100, 1,0,p4
    elif    direccion == 4: return  1,0,p3-80, 1,0,p2
    elif    direccion == 5: return  1,0,p3-70, 1,0,p1
    elif    direccion == 6: return  0,1,p5-100, 1,0,p5
    elif    direccion == 7: return  0,1,p5-100, 1,0,p5
    elif    direccion == 9: return  1,0,p5-100, 0,1,p5
    else:   return 0,0,0,0,0,0; #l_forw, l_back, l_velocidad, r_forw, r_back, r_velocidad

def regular_sentido_motores(pin_M_L_forw,pin_M_L_back,L_forw,L_back, pin_M_R_forw,pin_M_R_back,R_forw,R_back):
    '''Ejecuta la configuración del sentido de las ruedas ingresada'''
    if L_forw==1 and L_back==0: #AVANZA
        pin_M_L_forw.on()
        pin_M_L_back.off()
    elif L_forw==0 and L_back==1: #RETROCEDE
        pin_M_L_forw.off()
        pin_M_L_back.on()
    else: #STOP
        pin_M_L_forw.off()
        pin_M_L_back.off()

    if R_forw==1 and R_back==0: #AVANZA
        pin_M_R_forw.on()
        pin_M_R_back.off()
    elif R_forw==0 and R_back==1: #RETROCEDE
        pin_M_R_forw.off()
        pin_M_R_back.on()
    else: #STOP
        pin_M_R_forw.off()
        pin_M_R_back.off()

def regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm, interrupcion , M_L_velocidad ,M_R_velocidad ):
    '''Ejecuta la velocidad para los PWM ingresadas, si es que no hay una interrupción ("interrupcion")'''
    if not interrupcion:
        pin_M_L_pwm.duty(M_L_velocidad)
        pin_M_R_pwm.duty(M_R_velocidad)
    else:
        pin_M_L_pwm.duty(0)
        pin_M_R_pwm.duty(0)