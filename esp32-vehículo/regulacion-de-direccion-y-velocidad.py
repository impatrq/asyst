#0: las ruedas se quedan quietas. 
#1: gira mucho a la izquierda
#2: gira un poco a la izquierda 
#3: sigue en línea recta
#4: gira un poco a la derecha
#5: gira mucho a la derecha
#7: gira 90° a la izquierda
#8: gira 180°
#9: gira 90° a la derecha

freq = 25000        #esta variable no se usa por ahora 
l_sentido = 0
l_velocidad = 0
r_sentido = 0
r_velocidad = 0
velocidad = 35000

p25 = int(velocidad/4)
p30 = int(velocidad/100)*30
p40 = int(velocidad/100)*40
p50 = int(velocidad/2)
p60 = int(velocidad/100)*60
p75 = int(velocidad/4)*3
p80 = int(velocidad/100)*80
p90 = int(velocidad/100)*90
p100 = velocidad

def regular_direccion(direccion):
    if      direccion == 1: return 1,p30, 1,p90 #Acá se usaría el comando ".duty()" para regular la velocidad
    elif    direccion == 2: return 1,p60, 1,p90
    elif    direccion == 3: return 1,p100, 1,p100
    elif    direccion == 4: return 1,p90, 1,p60
    elif    direccion == 5: return 1,p90, 1,p30
    elif    direccion == 7: return 0,p40, 1,p80
    elif    direccion == 8: return 0,p75, 1,p75
    elif    direccion == 9: return 1,p80, 0,p40
    else:   return 1,0,1,0;

while 1:
    direccion = int(input("Ingrese dirección del carrito: "))
    l_sentido, l_velocidad, r_sentido, r_velocidad = regular_direccion(direccion)
    print("Izquierda:", l_sentido, "-", l_velocidad)
    print("Derecha:",   r_sentido, "-", r_velocidad)
