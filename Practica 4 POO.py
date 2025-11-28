from machine import Pin, ADC
import time
import dht

# ==========================================================
# CLASE BASE (HERENCIA + POLIMORFISMO)
# ==========================================================

class Sensor:
    def __init__(self, pin):
        self._pin = pin   # Atributo encapsulado

    def iniciar(self):
        pass  # Se sobreescribe

    def leer(self):
        raise NotImplementedError("Método leer() debe implementarse en la clase hija")

    def getPin(self):
        return self._pin


# ==========================================================
# SENSOR IR
# ==========================================================

class SensorIR(Sensor):
    def iniciar(self):
        self.pin = Pin(self._pin, Pin.IN)

    def leer(self):
        valor = self.pin.value()
        return "NO OBJETO" if valor == 1 else "OBJETO"


# ==========================================================
# SENSOR ULTRASÓNICO HC-SR04
# ==========================================================

class SensorUltrasonico(Sensor):
    def __init__(self, trig, echo):
        super().__init__(trig)
        self._echo = echo

    def iniciar(self):
        self.trig = Pin(self._pin, Pin.OUT)
        self.echo = Pin(self._echo, Pin.IN)

    def leer(self):
        # Pulso de disparo
        self.trig.value(0)
        time.sleep_us(5)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        # Espera de pulso (timeout manual)
        inicio = time.ticks_us()
        while self.echo.value() == 0:
            if time.ticks_diff(time.ticks_us(), inicio) > 25000:
                return "SIN LECTURA"

        start = time.ticks_us()

        while self.echo.value() == 1:
            if time.ticks_diff(time.ticks_us(), start) > 25000:
                return "SIN LECTURA"

        end = time.ticks_us()

        duracion = time.ticks_diff(end, start)

        distancia = (duracion * 0.0343) / 2
        return "{:.2f} cm".format(distancia)


# ==========================================================
# SENSOR LDR (ANALÓGICO)
# ==========================================================

class SensorLDR(Sensor):
    def iniciar(self):
        self.adc = ADC(Pin(self._pin))
        self.adc.atten(ADC.ATTN_11DB)  # Permite medir hasta ~3.3V

    def leer(self):
        valor = self.adc.read()
        return str(valor)


# ==========================================================
# SENSOR DHT11
# ==========================================================

class SensorDHT(Sensor):
    def iniciar(self):
        self.dht_sensor = dht.DHT11(Pin(self._pin))

    def leer(self):
        try:
            self.dht_sensor.measure()
            t = self.dht_sensor.temperature()
            h = self.dht_sensor.humidity()
            return "T={}C  H={}%".format(t, h)
        except:
            return "ERROR"


# ==========================================================
# CREACIÓN DE OBJETOS
# ==========================================================

ir1 = SensorIR(15)
ir2 = SensorIR(26)
ultra = SensorUltrasonico(14, 27)
ldr = SensorLDR(34)
dhtSensor = SensorDHT(4)

sensores = [ir1, ir2, ultra, ldr, dhtSensor]


# ==========================================================
# SETUP
# ==========================================================

print("=== SISTEMA POO - RED DE SENSORES (MicroPython) ===")

for s in sensores:
    s.iniciar()


# ==========================================================
# LOOP
# ==========================================================

while True:
    print("\n--------- LECTURA DE SENSORES ---------")
    print("IR1 (15):", ir1.leer())
    print("IR2 (26):", ir2.leer())
    print("Ultrasonico (14/27):", ultra.leer())
    print("LDR (34):", ldr.leer())
    print("DHT11 (4):", dhtSensor.leer())
    print("----------------------------------------")

    time.sleep(0.6)
