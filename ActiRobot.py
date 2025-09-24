""""- Una **clase** se define con la palabra clave `class`.
- El método especial `__init__` es el **constructor**, se ejecuta al crear un objeto.
- `self` representa al propio objeto (instancia).
- Un **objeto** se crea llamando a la clase como si fuera una función:  
  `mi_robot = Robot("R2D2", 100)`
PROGRAMACIÓN ORIENTADA A OBJETOS (POO)
│
├── CLASE
│   ├─ Es un molde o plano
│   ├─ Define atributos y métodos
│   └─ Ejemplo: class Robot:
│
├── OBJETO
│   ├─ Es una instancia de una clase
│   ├─ Se crea con: mi_robot = Robot("R2D2", 100)
│   └─ Tiene estado y comportamiento
│
├── ATRIBUTOS
│   ├─ Variables internas del objeto
│   ├─ Se definen en __init__ con self.atributo
│   └─ Ejemplo: self.nombre, self.bateria
│
├── MÉTODOS
│   ├─ Funciones dentro de la clase
│   ├─ Operan sobre los atributos
│   └─ Ejemplo: def encender(self):
│
├── ENCAPSULAMIENTO
│   ├─ Protege atributos internos
│   ├─ Se usa _atributo o propiedades (@property)
│   └─ Permite validación y control
│
├── HERENCIA
│   ├─ Una clase puede extender otra
│   ├─ Se usa: class SubClase(SuperClase):
│   ├─ Reutiliza atributos y métodos
│   └─ Ejemplo: class RobotMovil(Robot):
│
├── SOBRESCRITURA
│   ├─ Redefine un método en la subclase
│   ├─ Permite comportamiento especializado
│   └─ Ejemplo: def describir(self):  # redefinido
│
├── POLIMORFISMO
│   ├─ Mismo método → diferentes respuestas
│   ├─ Se usa en listas de objetos
│   └─ Ejemplo: for r in robots: r.describir()
│
└── MÉTODOS ESPECIALES
    ├─ __init__: constructor
    ├─ __str__: representación textual
    ├─ __repr__: depuración
    └─ __eq__: comparación de objetos
  
"""
# Definimos la clase base 'Robot'
class Robot:
    """
    Clase que representa un robot genérico.
    Tiene un nombre y un nivel de batería.
    """

    def __init__(self, nombre, bateria=100):
        # Guardamos el nombre del robot en un atributo
        self.nombre = nombre
        # Guardamos la batería inicial (por defecto 100)
        self.bateria = bateria
        # Estado inicial: apagado
        self.encendido = False

    def encender(self):
        # Solo puede encenderse si hay batería
        if self.bateria > 0:
            self.encendido = True
            print(f"{self.nombre} está encendido.")
        else:
            print(f"{self.nombre} no puede encenderse: batería agotada.")

    def apagar(self):
        # Cambiamos el estado a apagado
        self.encendido = False
        print(f"{self.nombre} se apagó.")

    def describir(self):
        # Devuelve un texto con la información del robot
        estado = "encendido" if self.encendido else "apagado"
        return f"Robot {self.nombre} | Batería: {self.bateria}% | Estado: {estado}"

    # Nuevo método 1: cargar batería
    def cargar_bateria(self, cantidad):
        """
        Recarga la batería del robot.
        """
        self.bateria = min(100, self.bateria + cantidad)
        print(f"{self.nombre} ha sido cargado. Batería actual: {self.bateria}%")

    # Nuevo método 2: saludar
    def saludar(self):
        """
        Hace que el robot salude.
        """
        print(f"Hola, soy {self.nombre} y estoy listo para servirte.")

# Creamos un objeto (instancia) de la clase Robot
robot1 = Robot("R2D2", bateria=80)

# Usamos sus métodos
print(robot1.describir())   # Muestra la información inicial
robot1.encender()           # Cambia el estado a encendido
print(robot1.describir())   # Ahora debe mostrar "encendido"
robot1.apagar()             # Cambia el estado a apagado

# Definimos una subclase que hereda de Robot
class RobotMovil(Robot):
    """
    Robot que puede moverse en un plano 2D.
    Hereda de Robot y añade atributos x, y.
    """

    def __init__(self, nombre, bateria=100, x=0, y=0):
        # Llamamos al constructor de la clase base
        super().__init__(nombre, bateria)
        # Añadimos atributos propios
        self.x = x
        self.y = y

    def mover(self, dx, dy):
        # Solo se mueve si está encendido
        if self.encendido and self.bateria > 0:
            self.x += dx
            self.y += dy
            # Cada movimiento consume 10% de batería
            self.bateria = max(0, self.bateria - 10)
            print(f"{self.nombre} se movió a ({self.x}, {self.y}).")
        else:
            print(f"{self.nombre} no puede moverse (apagado o sin batería).")

    # Sobrescribimos el método describir
    def describir(self):
        estado = "encendido" if self.encendido else "apagado"
        return (f"RobotMovil {self.nombre} | Posición: ({self.x}, {self.y}) | "
                f"Batería: {self.bateria}% | Estado: {estado}")

# Creamos un objeto de tipo RobotMovil
robot2 = RobotMovil("Wall-E", bateria=50)

print(robot2.describir())  # Muestra la información inicial
robot2.encender()          # Encendemos el robot
robot2.mover(2, 3)         # Lo movemos en el plano
print(robot2.describir())  # Ahora debe mostrar la nueva posición y batería

# Creamos dos nuevos robots de la clase Robot
robot3 = Robot("Robocop", bateria=70)
robot4 = Robot("Robot IIE", bateria=90)

# Probamos los nuevos métodos en los robots nuevos
robot3.saludar()
robot3.cargar_bateria(20)

robot4.saludar()
robot4.encender()
print(robot4.describir())

# Creamos una lista con robots de distintos tipos
robots = [robot1, robot2, robot3, robot4]

# Recorremos la lista y llamamos al mismo método 'describir'
for r in robots:
    print(r.describir())  # Cada objeto responde según su clase
