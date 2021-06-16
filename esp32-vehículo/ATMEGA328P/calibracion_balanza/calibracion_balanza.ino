#include "HX711.h"

// Pin de datos y de reloj
byte pinData = 3;
byte pinClk = 2;

HX711 bascula;

// Parámetro para calibrar el peso y el sensor
float factor_calibracion = 20780.0; //Este valor del factor de calibración funciona para mi. El tuyo probablemente será diferente.

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 programa de calibracion");
  Serial.println("Quita cualquier peso de la bascula");
  Serial.println("Una vez empiece a mostrar informacion de medidas, coloca un peso conocido encima de la bascula");
  Serial.println("Presiona + para incrementar el factor de calibracion");
  Serial.println("Presiona - para disminuir el factor de calibracion");

  // Iniciar sensor
  bascula.begin(pinData, pinClk);

  // Aplicar la calibración
  bascula.set_scale();
  // Iniciar la tara
  // No tiene que haber nada sobre el peso
  bascula.tare();

  // Obtener una lectura de referencia
  long zero_factor = bascula.read_average();
  // Mostrar la primera desviación
  Serial.print("Zero factor: ");
  Serial.println(zero_factor);
}

void loop() {

  // Aplicar calibración
  bascula.set_scale(factor_calibracion);

  // Mostrar la información para ajustar el factor de calibración
  Serial.print("Leyendo: ");
  Serial.print(bascula.get_units(), 1);
  Serial.print(" kgs");
  Serial.print(" factor_calibracion: ");
  Serial.print(factor_calibracion);
  Serial.println();

  // Obtener información desde el monitor serie
  if (Serial.available())
  {
    char temp = Serial.read();
    if (temp == '+')
      factor_calibracion += 10;
    else if (temp == '-')
      factor_calibracion -= 10;
      serial.print(factor_calibration)
  }
}
