#----------------------Librerías a utilizar-----------------------
from machine import Pin, PWM, ADC, time 
import time
import libs_asyst as lib
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

#----------------Variables y objetos a utilizar---------------------
direccion = 0
destino = []   #Próximamente se le preguntará al servidor el destino
countIman = 0
posicion_actual = []
destinoPanol = []
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

#pines = [boton_frenado,sensor_IFR, alarma_balanza, sensor_MG]
#--------------------------------------------------------------
def main():
    while 1:
        boton_frenado, sensor_IFR, alarma_balanza, sensor_MG = lib.actualizar_valores(pin_boton_frenado,pin_sensor_IFR, pin_alarma_balanza, pin_sensor_MG)
        direccion = lib.corregir_rumbo(sensor_IFR)
        if sensor_MG:
            posicion_actual, direccion, countIman, destino = lib.reconocimiento_sector(destino,countIman,destinoPanol,posicion_actual)
        interrupcion = lib.frenado_emergencia(boton_frenado,sensor_US)
        interrupcion += alarma_balanza
        M_L_sentido,M_L_pwm,M_R_sentido,M_R_pwm = lib.regular_direccion(direccion,velocidades_dict)
        lib.regular_sentido_motores(pin_M_L_sentido,pin_M_R_sentido,M_L_sentido,M_R_sentido)
        lib.regular_velocidad_motores(pin_M_L_pwm,pin_M_R_pwm,interrupcion,M_L_pwm,M_R_pwm)

        pass

main()

#!Esperar y averiguar dónde es necesario un time.sleep()