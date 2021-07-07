from os import stat_result
from machine import Pin, time
import json
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
def actualizar_valores(pin_boton_frenado,pin_sensor_IFR, pin_alarma_balanza, pin_sensor_MG):#todo:usado
    boton_frenado = pin_boton_frenado.value()
    sensor_IFR = [0,0,0,0,0]
    for i in range (5):
        sensor_IFR[i] = pin_sensor_IFR[i].value()
    alarma_balanza = pin_alarma_balanza.value()
    sensor_MG = pin_sensor_MG.value()
    return boton_frenado,sensor_IFR,alarma_balanza,sensor_MG;

def corregir_rumbo(aux):#todo:usado  #ingresa una lista con los valores 1/0 de los sensores Infrarrojos.
    if   aux==[0,0,0,0,1]: return 5; #gira mucho a la derecha
    elif aux==[0,0,0,1,1]: return 5; #gira mucho a la derecha
    elif aux==[0,1,1,1,1]: return 4; #gira un poco a la derecha
    elif aux==[0,0,1,1,1]: return 4; #gira un poco a la derecha
    elif aux==[0,0,1,1,0]: return 4; #gira un poco a la derecha
    elif aux==[0,1,1,1,0]: return 3; #Avanza en línea recta
    elif aux==[1,1,1,0,0]: return 2; #gira un poco a la izquierda
    elif aux==[0,1,1,0,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,1,1,1,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,1,0,0,0]: return 1; #gira mucho a la izquierda
    elif aux==[1,0,0,0,0]: return 1; #gira mucho a la izquierda
    else: return 8; #Perdido D:

def crear_posicion(destino):#*Función auxiliar opcional
    posicion_actual = []
    destinoPañol = []
    for i in range (len(destino)): 
        destino[i] = int(destino[i])
        destinoPañol.append(0) 
        posicion_actual.append(-1)
    return destinoPañol, posicion_actual;#Esto se puede modificar

def frenado_emergencia(boton_frenado, sensor_US):#todo:usado
    distancia = sensor_US.distance_cm() #Recordar crear el objeto de sensor_US
    if distancia>=100 and boton_frenado==0:
        return 0;
    else: 
        return 1;

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

def reconocimiento_sector(destino, countIman, destinoPañol, posicion_actual,server_send_dict):#todo:usado

    if destino == destinoPañol:
        countIman -= 1
        posicion_actual[0] = countIman
        if (countIman > destino[0]) and (posicion_actual != destino):
            if      posicion_actual[countIman] == 7: auxDireccion = 9
            elif    posicion_actual[countIman] == 9: auxDireccion = 7
            else:   auxDireccion = 3
            posicion_actual[countIman] = 0
            return posicion_actual, auxDireccion, countIman, destino,server_send_dict
        else: #posicion_actual==destino: 
            #print("Llegamos al Pañol")
            server_send_dict['posicion_actual'] = posicion_actual #tiene que ser 0,0,0,0,0
            #Actualizar destino
            return posicion_actual, 0, countIman, destino,server_send_dict

    else:
        countIman += 1
        posicion_actual[0] = countIman
        if (countIman < destino[0]) and (posicion_actual != destino):  
            posicion_actual[countIman] = destino[countIman]
            return posicion_actual, destino[countIman], countIman, destino, server_send_dict
        else: #posicion_actual == destino
            server_send_dict['posicion_actual'] = posicion_actual #tiene que ser !!0,0,0,0,0!!
            #print("Llegamos a destino")
            destino = destinoPañol
            return posicion_actual, 0, countIman, destino, server_send_dict 

def regular_direccion(direccion, velocidades_dict): #todo:usado  /// Recordar importar las los valores de "p" como un diccionario
    if      direccion == 1: return  1,velocidades_dict['p30'], 1,velocidades_dict['p90'] #Acá se usaría el comando ".duty()" para regular la velocidad
    elif    direccion == 2: return  1,velocidades_dict['p60'], 1,velocidades_dict['p90']
    elif    direccion == 3: return 1,velocidades_dict['p100'],1,velocidades_dict['p100']
    elif    direccion == 4: return  1,velocidades_dict['p90'], 1,velocidades_dict['p60']
    elif    direccion == 5: return  1,velocidades_dict['p90'], 1,velocidades_dict['p30']
    elif    direccion == 7: return  0,velocidades_dict['p40'], 1,velocidades_dict['p80']
    #elif    direccion == 8: return  0,velocidades_dict['p75'], 1,velocidades_dict['p75']
    elif    direccion == 9: return  1,velocidades_dict['p60'], 0,velocidades_dict['p40']
    else:   return 1,0,1,0; #l_sentido, l_velocidad, r_sentido, r_velocidad

def regular_sentido_motores(pin_M_L_sentido,pin_M_R_sentido,L_sentido,R_sentido):#todo:usado
    if L_sentido == 1: pin_M_L_sentido.on()
    else: pin_M_L_sentido.off()
    if R_sentido == 1: pin_M_R_sentido.on()
    else: pin_M_R_sentido.off()

def regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm, interrupcion, M_L_velocidad,M_R_velocidad ):#todo:usado
    if interrupcion == 0:
        pin_M_L_pwm.duty(M_L_velocidad)
        pin_M_R_pwm.duty(M_R_velocidad)
    else:
        pin_M_L_pwm.duty(0)
        pin_M_R_pwm.duty(0)




    