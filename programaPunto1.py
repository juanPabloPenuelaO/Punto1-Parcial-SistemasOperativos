class Proceso:
    def __init__(self, pid):
        self.pid = pid
        self.estado = "Nuevo"
        self.historial = [self.estado]

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.historial.append(nuevo_estado)
        print(f"Proceso {self.pid} → Estado: {nuevo_estado}")

class GestorProcesos:
    def __init__(self):
        self.procesos = []

    def crear_proceso(self, pid):
        p = Proceso(pid)
        self.procesos.append(p)
        return p

    def ejecutar(self, proceso):
        proceso.cambiar_estado("Listo")
        proceso.cambiar_estado("Ejecutando")

        # Simulación de evento aleatorio
        from random import choice
        evento = choice(["espera", "termina"])

        if evento == "espera":
            proceso.cambiar_estado("Esperando")
            proceso.cambiar_estado("Listo")  # vuelve a listo después de esperar
            proceso.cambiar_estado("Ejecutando")
        
        proceso.cambiar_estado("Terminado")

    def mostrar_historial(self):
        for p in self.procesos:
            print(f"\nHistorial del proceso {p.pid}: {p.historial}")

# Simulación
sistema = GestorProcesos()
p1 = sistema.crear_proceso(1)
p2 = sistema.crear_proceso(2)

sistema.ejecutar(p1)
sistema.ejecutar(p2)

sistema.mostrar_historial()
