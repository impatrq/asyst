#El sernsor envía un 1 cuando detecta negro
#Parte para la simulación (a borrar próximamente)
HIGH = 1
LOW = 0
ifr=[0,0,0,0,0]
#Parte que va en el código
def corregir_rumbo(aux):
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
    else: print("      a       , me predí D: (función a realizar posiblemente)")

#Parte para la simulación (a borrar próximamente)
while (1):
    ifr[0]=int(input("1:"))
    ifr[1]=int(input("2:"))
    ifr[2]=int(input("3:"))
    ifr[3]=int(input("4:"))
    ifr[4]=int(input("5:"))
    direccion = corregir_rumbo(ifr)
    print("dirección:", direccion)

