class Proceso:
    """Clase para representar un proceso en el sistema."""
    
    def __init__(self, nombre, tiempo_llegada, tiempo_rafaga):
        """
        Inicializa un proceso.
        
        Args:
            nombre: Identificador del proceso
            tiempo_llegada: Momento en que el proceso llega al sistema
            tiempo_rafaga: Tiempo total de CPU que necesita el proceso
        """
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_rafaga = tiempo_rafaga
        self.tiempo_rafaga_restante = tiempo_rafaga
        self.tiempo_espera = 0
        self.tiempo_respuesta = -1  # -1 indica que aún no ha comenzado
        self.tiempo_finalizacion = 0
        self.tiempo_ejecucion = 0  # Turnaround time


def round_robin(procesos, quantum):
    """
    Ejecuta el algoritmo de planificación Round Robin.
    
    Args:
        procesos: Lista de objetos Proceso ordenados por tiempo de llegada
        quantum: Tiempo de quantum asignado a cada proceso
    
    Returns:
        Lista de procesos con las métricas calculadas
    """
    # Crear una copia de los procesos para no modificar los originales
    procesos_copia = []
    for p in procesos:
        nuevo_proceso = Proceso(p.nombre, p.tiempo_llegada, p.tiempo_rafaga)
        procesos_copia.append(nuevo_proceso)
    
    # Cola de procesos listos
    cola_listos = []
    procesos_completados = []
    tiempo_actual = 0
    indice_proceso = 0
    
    # Ordenar procesos por tiempo de llegada
    procesos_copia.sort(key=lambda x: x.tiempo_llegada)
    
    print("\n=== Simulación Round Robin ===\n")
    print(f"Quantum: {quantum} unidades de tiempo\n")
    
    while indice_proceso < len(procesos_copia) or cola_listos:
        # Agregar procesos que han llegado al sistema
        while (indice_proceso < len(procesos_copia) and 
               procesos_copia[indice_proceso].tiempo_llegada <= tiempo_actual):
            proceso = procesos_copia[indice_proceso]
            cola_listos.append(proceso)
            print(f"Tiempo {tiempo_actual}: {proceso.nombre} llega al sistema")
            indice_proceso += 1
        
        if cola_listos:
            # Obtener el siguiente proceso de la cola
            proceso_actual = cola_listos.pop(0)
            
            # Marcar tiempo de respuesta si es la primera vez que se ejecuta
            if proceso_actual.tiempo_respuesta == -1:
                proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.tiempo_llegada
            
            # Ejecutar el proceso por el quantum o hasta que termine
            tiempo_ejecutado = min(quantum, proceso_actual.tiempo_rafaga_restante)
            tiempo_inicio = tiempo_actual
            
            print(f"Tiempo {tiempo_actual}: {proceso_actual.nombre} comienza ejecución "
                  f"(tiempo restante: {proceso_actual.tiempo_rafaga_restante})")
            
            tiempo_actual += tiempo_ejecutado
            proceso_actual.tiempo_rafaga_restante -= tiempo_ejecutado
            
            # Actualizar tiempo de espera de los procesos en la cola
            for proceso_en_cola in cola_listos:
                proceso_en_cola.tiempo_espera += tiempo_ejecutado
            
            print(f"Tiempo {tiempo_actual}: {proceso_actual.nombre} termina ejecución "
                  f"(tiempo restante: {proceso_actual.tiempo_rafaga_restante})")
            
            # Si el proceso terminó
            if proceso_actual.tiempo_rafaga_restante == 0:
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_ejecucion = tiempo_actual - proceso_actual.tiempo_llegada
                procesos_completados.append(proceso_actual)
                print(f"Tiempo {tiempo_actual}: {proceso_actual.nombre} COMPLETADO")
            else:
                # El proceso vuelve a la cola
                cola_listos.append(proceso_actual)
                print(f"Tiempo {tiempo_actual}: {proceso_actual.nombre} vuelve a la cola")
        else:
            # No hay procesos listos, avanzar el tiempo
            if indice_proceso < len(procesos_copia):
                tiempo_actual = procesos_copia[indice_proceso].tiempo_llegada
    
    return procesos_completados


def calcular_metricas(procesos):
    """
    Calcula y muestra las métricas de los procesos.
    
    Args:
        procesos: Lista de procesos completados
    """
    print("\n" + "="*80)
    print("MÉTRICAS DE LOS PROCESOS")
    print("="*80)
    print(f"{'Proceso':<10} {'Llegada':<10} {'Ráfaga':<10} {'Finalización':<15} "
          f"{'Espera':<10} {'Ejecución':<12} {'Respuesta':<10}")
    print("-"*80)
    
    tiempo_espera_total = 0
    tiempo_ejecucion_total = 0
    tiempo_respuesta_total = 0
    
    for proceso in procesos:
        tiempo_espera_total += proceso.tiempo_espera
        tiempo_ejecucion_total += proceso.tiempo_ejecucion
        tiempo_respuesta_total += proceso.tiempo_respuesta
        
        print(f"{proceso.nombre:<10} {proceso.tiempo_llegada:<10} {proceso.tiempo_rafaga:<10} "
              f"{proceso.tiempo_finalizacion:<15} {proceso.tiempo_espera:<10} "
              f"{proceso.tiempo_ejecucion:<12} {proceso.tiempo_respuesta:<10}")
    
    num_procesos = len(procesos)
    tiempo_espera_promedio = tiempo_espera_total / num_procesos
    tiempo_ejecucion_promedio = tiempo_ejecucion_total / num_procesos
    tiempo_respuesta_promedio = tiempo_respuesta_total / num_procesos
    
    print("-"*80)
    print(f"\nMÉTRICAS PROMEDIO:")
    print(f"  Tiempo de espera promedio: {tiempo_espera_promedio:.2f}")
    print(f"  Tiempo de ejecución promedio (Turnaround): {tiempo_ejecucion_promedio:.2f}")
    print(f"  Tiempo de respuesta promedio: {tiempo_respuesta_promedio:.2f}")
    print("="*80 + "\n")


def main():
    """Función principal para demostrar el uso del algoritmo Round Robin."""
    
    # Ejemplo 1: Procesos con diferentes tiempos de llegada y ráfaga
    print("\n" + "="*80)
    print("EJEMPLO 1: Procesos con diferentes características")
    print("="*80)
    
    procesos1 = [
        Proceso("P1", 0, 5),   # Llega en 0, necesita 5 unidades
        Proceso("P2", 1, 3),   # Llega en 1, necesita 3 unidades
        Proceso("P3", 2, 8),   # Llega en 2, necesita 8 unidades
        Proceso("P4", 3, 6),   # Llega en 3, necesita 6 unidades
    ]
    
    quantum1 = 4
    procesos_completados1 = round_robin(procesos1, quantum1)
    calcular_metricas(procesos_completados1)
    
    # Ejemplo 2: Procesos que llegan todos al mismo tiempo
    print("\n" + "="*80)
    print("EJEMPLO 2: Todos los procesos llegan al mismo tiempo")
    print("="*80)
    
    procesos2 = [
        Proceso("A", 0, 10),
        Proceso("B", 0, 5),
        Proceso("C", 0, 8),
    ]
    
    quantum2 = 3
    procesos_completados2 = round_robin(procesos2, quantum2)
    calcular_metricas(procesos_completados2)


if __name__ == "__main__":
    main()

