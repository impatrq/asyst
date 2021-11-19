import machine
import ujson
import network                            # importa el módulo network
import urequests
import time

sta_if = network.WLAN(network.STA_IF);    # instancia el objeto -sta_if- para controlar la interfaz STA
sta_if.active(True)                       # activa la interfaz STA del ESP32
if sta_if.isconnected(): sta_if.disconnect()
sta_if.connect("Avionica-2", "Atlantida2020")    # inicia la conexión con el AP, "nombre - contraseña" de red
while not sta_if.isconnected():
    time.sleep(0.5)
