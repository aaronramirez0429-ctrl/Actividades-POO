#include <Arduino.h>   // Librería base para usar funciones de Arduino
#include <DHT.h>       // Librería para sensores DHT11 / DHT22


/*
==========================================================
=                CONCEPTOS DE POO USADOS                =
==========================================================
* CLASES: Definimos la base Sensor y todas las derivadas.
* OBJETOS: Creamos objetos de cada sensor en setup().
* HERENCIA: Las clases hijas heredan de Sensor.
* ENCAPSULAMIENTO: Atributos privados con getters.
* POLIMORFISMO: leer() se sobreescribe en cada sensor.
==========================================================
*/


// ********* CLASE BASE (HERENCIA + POLIMORFISMO) *********

class Sensor {
  protected:
    int pin;           // Atributo protegido: lo heredan los hijos

  public:
    // Constructor que recibe el pin del sensor
    Sensor(int p) : pin(p) {}

    // Método virtual: permite polimorfismo
    virtual void iniciar() {}

    // Método virtual puro: obliga a las clases hijas a implementarlo
    virtual String leer() = 0;

    // Getter (encapsulamiento)
    int getPin() { return pin; }
};


// ********* SENSOR IR (HEREDA DE SENSOR) *********

class SensorIR : public Sensor {
  public:
    // Constructor pasa el pin al constructor padre
    SensorIR(int p) : Sensor(p) {}

    // Configura el pin como entrada
    void iniciar() override {
      pinMode(pin, INPUT);
    }

    // Lee el estado digital del infrarrojo
    String leer() override {
      int valor = digitalRead(pin);
      // En sensores IR LOW = objeto detectado
      return valor ? "NO OBJETO" : "OBJETO";
    }
};


// ********* SENSOR ULTRASÓNICO (TRIGGER + ECHO) *********

class SensorUltrasonico : public Sensor {
  private:
    int pinEcho;   // Pin adicional (encapsulado)

  public:
    // Constructor recibe TRIG y ECHO
    SensorUltrasonico(int trig, int echo) : Sensor(trig), pinEcho(echo) {}

    // Configura TRIG como salida y ECHO como entrada
    void iniciar() override {
      pinMode(pin, OUTPUT);
      pinMode(pinEcho, INPUT);
    }

    // Función de lectura del sensor ultrasonico
    String leer() override {

      // Pulso de disparo del TRIG
      digitalWrite(pin, LOW);
      delayMicroseconds(5);
      digitalWrite(pin, HIGH);
      delayMicroseconds(10);
      digitalWrite(pin, LOW);

      // Lee el tiempo del pulso del eco
      long duracion = pulseIn(pinEcho, HIGH, 25000);

      // Si no hubo lectura
      if (duracion == 0) return "SIN LECTURA";

      // Calcula distancia en cm
      float distancia = duracion * 0.034 / 2;

      return String(distancia) + " cm";
    }
};


// ********* SENSOR LDR (ANALÓGICO) *********

class SensorLDR : public Sensor {
  public:
    SensorLDR(int p) : Sensor(p) {}

    // LDR no necesita configuración especial
    void iniciar() override {
      pinMode(pin, INPUT);
    }

    // Lectura analógica y la devuelve como String
    String leer() override {
      int valor = analogRead(pin);
      return String(valor);
    }
};


// ********* SENSOR DHT11 *********

class SensorDHT : public Sensor {
  private:
    DHT dht;   // Objeto DHT encapsulado dentro de la clase

  public:
    // Constructor inicializa DHT con el pin y tipo DHT11
    SensorDHT(int p) : Sensor(p), dht(p, DHT11) {}

    // Inicializa el sensor
    void iniciar() override {
      dht.begin();
    }

    // Lee temperatura y humedad
    String leer() override {
      float t = dht.readTemperature();
      float h = dht.readHumidity();

      // Si hay error de lectura
      if (isnan(t) || isnan(h)) return "ERROR";

      return "T=" + String(t) + "C  H=" + String(h) + "%";
    }
};




// ==========================================================
//      CREACIÓN DE OBJETOS (INSTANCIAS DE LAS CLASES)
// ==========================================================

SensorIR ir1(15);                 // Sensor IR en pin 15
SensorIR ir2(26);                 // Sensor IR en pin 26
SensorUltrasonico ultra(14, 27);  // TRIG=14, ECHO=27
SensorLDR ldr(34);                // LDR en pin 34
SensorDHT dhtSensor(4);           // DHT11 en pin 4

// Arreglo polimórfico: almacena objetos de distintas clases
Sensor* sensores[] = { &ir1, &ir2, &ultra, &ldr, &dhtSensor };
int totalSensores = 5;



// ========================= SETUP =========================

void setup() {
  Serial.begin(115200);    // Inicia monitor serie
  Serial.println("=== SISTEMA POO - RED DE SENSORES ===");

  // Inicializa todos los sensores usando polimorfismo
  for (int i = 0; i < totalSensores; i++) {
    sensores[i]->iniciar();
  }
}



// ========================= LOOP =========================

void loop() {

  Serial.println("\n--------- LECTURA DE SENSORES ---------");

  // Se llaman directamente los métodos leer() de cada sensor
  Serial.print("IR1 (15): ");
  Serial.println(ir1.leer());

  Serial.print("IR2 (26): ");
  Serial.println(ir2.leer());

  Serial.print("Ultrasonico (14/27): ");
  Serial.println(ultra.leer());

  Serial.print("LDR (34): ");
  Serial.println(ldr.leer());

  Serial.print("DHT11 (4): ");
  Serial.println(dhtSensor.leer());

  Serial.println("----------------------------------------");

  delay(600);   // Espera antes de repetir
}
