#include "HX711.h"
#define DEBUG_HX711
//------------------
#include  <Wire.h>
#include  <LiquidCrystal_I2C.h>
//LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Parámetro para calibrar el peso y el sensor
#define CALIBRACION1 20780.0           //MODIFICAR ESTE VALOR DEPENDIENDO EL VALOR OBTENIDO EN LA ETAPA DE CALIBRACIÓN
#define CALIBRACION2 20780.0
// Pin de datos y de reloj
byte pinData = 3;
byte pinClk = 2;
byte pinData2 = 4;
byte pinClk2= 5;
// Objeto HX711
HX711 Bascula;
HX711 Bascula2;
//pines y variables de Buzzer
unsigned int freq = 20000;      //probar la freq del buzzer y cualquier cosa cambiar

#define buzzer 13
 
void setup() {
  pinMode(13, OUTPUT);             //Chequear si el 8 está disponible
  
  //-------------------------DISPLAY-----------------------
  // Indicar a la libreria que tenemos conectada una pantalla de 16x2
  //lcd.begin(16, 2);          //PUEDE SER QUE SEA NECESARIO AÑADIR ESTA LINEA Y LA N°6, SACANDO LA 7

  //lcd.init();
  lcd.backlight();    //¿QUEREMOS BACKLIGHT?
  lcd.clear();

  // Mover el cursor a la primera posición de la pantalla (0, 0)
  lcd.home ();
  // Imprimir "Hola Mundo" en la primera linea
  lcd.print("INICIANDO...");
  //-- Mover el cursor a la segunda linea (1) primera columna
  //lcd.setCursor ( 0, 1 );
  // Mover el cursor a la primera posición de la pantalla (0, 0)
  //lcd.clear();

  //-------------------------BÁSCULA-----------------------
  // Iniciar sensor
  Bascula.begin(pinData, pinClk);
  Bascula2.begin(pinData2, pinCLk2);
  // Aplicar la calibración
  Bascula.set_scale(CALIBRACION1);
  Bascula2.set_scale(CALIBRACION2);
  // Iniciar la tara
  // No tiene que haber nada sobre el peso
  Bascula.tare();
  Bascula2.tare()
}
 
void loop() {
  lcd.clear(); //limpio la pantalla (creo XD)
#ifdef DEBUG_HX711  //probablemente borrar

  float peso1 = Bascula.get_units();
  float peso2 = Bascula2.get_units();
  float peso = (peso1+peso2)/2

if (peso>=80){
    while (peso>=80){
      //imprimo el peso abajo
      lcd.setCursor(1,1);
      lcd.print(peso);
      //imprimo una alerta arriba y la borro después de un delay (titila)
      lcd.setCursor(1,0);
      lcd.print("PESO EXCEDIDO");
      delay (1000);
      tone(buzzer, freq, 1000);
      delay(500);
      lcd.clear();
      delay(500);
      
      //limpio la pantalla (creo XD) y actualizo la variable "peso"
      lcd.clear();
      peso1 = Bascula.get_units(); 
      peso2 = Bascula2.get_units();
      peso = (peso1+peso2)/2

    }
  }
else{
    noTone(buzzer); //se podría borrar 
    //Posiciono en segunda columna, segunda fila (cuento desde 0)
    lcd.setCursor(1,1);
    lcd.print(peso);
    
    delay(500);
  }
  

#endif    //probablemente borrar
}
