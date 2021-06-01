#datos de entrada: código del destino, detección de imán. 
#datos de salida: código de posición actual.
#3 para seguir derecho
#7 para girar 90° a la izquierda
#9 para girar 90° a la derecha
destinoPañol = []
posicion_actual = []
countIman = 0
auxDireccion = 0
destino = list(input("Ingrese dirección del destino: "))
for i in range (len(destino)): 
    destino[i] = int(destino[i])
    destinoPañol.append(0) 
    posicion_actual.append(-1) 
print(destino, posicion_actual)

#Acá EMPIEZA la función que iría dentro del programa real
def reconocimiento_sector(destino, iman, countIman):
    if iman == 1:

        if destino == destinoPañol:
            countIman -= 1
            posicion_actual[0] = countIman
            if (countIman > destino[0]) and (posicion_actual != destino):
                if      posicion_actual[countIman] == 7: auxDireccion = 9
                elif    posicion_actual[countIman] == 9: auxDireccion = 7
                else:   auxDireccion = 3
                posicion_actual[countIman] = 0
                return posicion_actual, auxDireccion, countIman, destino
            elif posicion_actual == destino: 
                print("Llegamos al Pañol")
                return posicion_actual, 0, countIman, destino

        else:
            countIman += 1
            posicion_actual[0] = countIman
            if (countIman < destino[0]) and (posicion_actual != destino):  
                posicion_actual[countIman] = destino[countIman]
                return posicion_actual, destino[countIman], countIman, destino
            else: 
                print("Llegamos a destino")
                destino = destinoPañol
                return posicion_actual, 0, countIman, destino

    else: return posicion_actual, 3, countIman, destino
#Acá TERMINA la función que iría dentro del programa real

while 1:
    iman = int(input("¿Hay algún imán? (1 para 'sí', 0 para 'no'): "))
    posicion_actual, direccion, countIman, destino = reconocimiento_sector(destino, iman, countIman)
    print(posicion_actual, "dirección:",direccion, "¿Hubo imán?:", iman, "Destino:", destino)