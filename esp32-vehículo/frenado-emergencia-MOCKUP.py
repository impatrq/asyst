#from .hcsr04 import HCSR04
#definir el trigger pin, el echo pin y el echo timeout
#luego crear la clase del HCSR04
def frenado_emergencia(boton_frenado, distancia):
    #distancia = sensor_US.distance_cm()
    try:
        if distancia>=100 and boton_frenado==False:
            print(boton_frenado)
            return 1;
        else: 
            print(boton_frenado)
            return 0;
    except:
        return "Error";

while 1:
    jorge_el_boton = bool(input("botón de frenado (1 o nada): ")) #jorge_el_boton = boton_frenado
    sensor_US = float(input("Ingrese valor de ultrasonido: "))
    resultado = frenado_emergencia(jorge_el_boton, sensor_US)
    if resultado == 1: print("El carrito avanza.")
    elif resultado == 0: print("El carrito NO avanza")
    else: print (resultado)

