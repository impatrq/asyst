import machine, time
from machine import Pin
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
    def __init__(self):
        self.get  = 'http://127.0.0.1:8000/prueba_read.json'#Cambiar por la url y el nombre del archivo a buscar
        self.post = ''
        matricula = 420
URL = URLs()

def p(velocidad):
    '''Devuelve una lista en la que cada posición corresponde a un porcentaje de la velocidad ingresada'''
    velocidad = int(velocidad)
    p = []
    for percent in range(101):
        aux1 = int((velocidad/100)*percent)
        p.append(aux1)
    return p

def actualizar_valores(pin_sensor_IFR=0, pin_alarma_balanza=0, pin_sensor_MG=0,pin_sensor_MG_2=0,pin_confirmacion=0):#todo:usado
    '''Actualiza los valores de los sensores IFR, la alarma de balanza y sensores magnéticos'''
    valores = []
    if pin_sensor_IFR:
        sensor_IFR = [0,0,0,0]
        for i in range (4):
            sensor_IFR[i] = pin_sensor_IFR[i].value()
        valores.append(sensor_IFR)
    if pin_alarma_balanza: 
        alarma_balanza = pin_alarma_balanza.value()
        valores.append(alarma_balanza)
    if pin_sensor_MG: 
        sensor_MG = pin_sensor_MG.value()
        valores.append(sensor_MG)
    if pin_sensor_MG_2: 
        sensor_MG_2 = pin_sensor_MG_2.value()
        valores.append(sensor_MG_2)
    if pin_confirmacion: 
        confirmacion = pin_confirmacion.value()
        valores.append(confirmacion)
    return valores

def corregir_rumbo(aux):#todo: usado  #ingresa una lista con los valores 1/0 de los sensores Infrarrojos.
    '''Devuelve una dirección en base a los sensores IFR'''
    if   aux==[0,0,0,1]: return 5; #gira mucho a la derecha
    elif aux==[0,0,1,1]: return 5; #gira un poco a la derecha
    elif aux==[0,1,1,1]: return 4; #gira un poco a la derecha
    elif aux==[0,1,1,0]: return 3; #linea recta
    elif aux==[1,1,1,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,1,0,0]: return 2; #gira un poco a la izquierda
    elif aux==[1,0,0,0]: return 1; #gira un poco a la izquierda
    else: return 8; #Perdido D:

def crear_posicion(carrito_dict):#*Función auxiliar opcional
    carrito_dict['posicion_actual'] = []
    destinoPanol = []
    for i in range (len(server_dict['destino'])): 
        server_dict['destino'][i] = int(server_dict['destino'][i])
        destinoPanol.append(0) 
        carrito_dict['posicion_actual'].append(-1)
    return destinoPanol, carrito_dict['posicion_actual'];#Esto se puede modificar

def frenado(sensor_US):#todo:usado
    distancia = sensor_US.distance_cm() #Recordar crear el objeto de sensor_US
    if distancia>=100: return 0;
    else: return 1;

def get_from_server():
    '''Obtiene un nuevo server_dict['destino'] y entrega/devolución del servidor'''
    #matricula, rumbo, ocupado, viajando, idavuelta, perdido
    info_dict = {}
    resp = urequests.get(URL.get).content
    resp=resp.decode("utf-8")
    print(resp)
    server_dict = ujson.loads(resp)
    destino = server_dict['rumbo'].split(",")
    for i in range(len(destino)):
        destino[i] = int(destino[i])
    return destino

def send_to_server(data:dict):
    '''Envía la información ingresada al servidor'''
    #nombres = ['ocupado', 'viajando', 'idavuelta','perdido','pos_actual']
    for i in data:
        key = i
    data = str(URL.matricula) + '-' + str(key) + '-' + str(data[key])
    resp = urequests.post(URL.post, data=data)
    resp.close()

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
def reconocimiento_sector(destino, countIman, destinoPanol,posicion_actual):#todo:usado

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
            return destino, auxDireccion, countIman,posicion_actual, delay
        elif posicion_actual == destino: 
            #print("Llegamos al Pañol")
            destino = None #Reseteo La variable de destino para esperar uno nuevo
            
            return destino, 6, countIman, posicion_actual,False

    else:
        countIman += 1
        posicion_actual[0] = countIman
        if (countIman < destino[0]) and (posicion_actual != destino):  
            posicion_actual[countIman] = destino[countIman]
            auxDireccion = int(posicion_actual[countIman])
            if auxDireccion==9 or auxDireccion==7: delay = True
            else: delay=False
            return destino, auxDireccion, countIman, posicion_actual,delay
        else: 
            #print("Llegamos a Destino")
            destino = destinoPanol
            send_to_server({'viajando':False})
            send_to_server({'iavuelta':True})
            return destino, 6, countIman, posicion_actual,False
            
def regular_direccion(direccion): #todo:usado            #Recordar importar las los valores de "p" como un diccionario
    '''Devuelve una configuración para las ruedas en base a la dirección y los porcentajes de potencia ingresados'''    
    rest = 22
    p1 = 40
    p2 = 60
    p3 = 75
    p4 = 80
    p5 = 40
    if      direccion == 1: return  1,0,p1-rest, 1,0,p3 
    elif    direccion == 2: return  1,0,p2-rest, 1,0,p3
    elif    direccion == 3: return  1,0,p4-rest, 1,0,p4
    elif    direccion == 4: return  1,0,p3-rest, 1,0,p2
    elif    direccion == 5: return  1,0,p3-rest, 1,0,p1
    elif    direccion == 6: return  0,1,p5-rest, 1,0,p5
    elif    direccion == 7: return  0,1,p5-rest, 1,0,p5
    elif    direccion == 9: return  1,0,p5-rest, 0,1,p5
    else:   return 0,0,0,0,0,0; #l_forw, l_back, l_velocidad, r_forw, r_back, r_velocidad

def regular_sentido_motores(pin_M_L_forw,pin_M_L_back,L_forw,L_back, pin_M_R_forw,pin_M_R_back,R_forw,R_back):#todo:usado
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

def regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm, interrupcion , M_L_velocidad ,M_R_velocidad ):#todo:usado
    '''Ejecuta la velocidad para los PWM ingresadas, si es que no hay una interrupción ("interrupcion")'''
    if not interrupcion:
        pin_M_L_pwm.duty(M_L_velocidad)
        pin_M_R_pwm.duty(M_R_velocidad)
    else:
        pin_M_L_pwm.duty(0)
        pin_M_R_pwm.duty(0)



