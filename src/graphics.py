# INPUT = Porcentaje de celdas vivas en el dominio inicial
# por lo menos 6 valores en el intervalo (0, 100%]
# Por ejemplo = {100, 85, 70, 55, 40, 25} (Menos no porque usualmente se mueren rapido, ya 25 parece poco)

# OUTPUT = Grilla en cada tiempo

# OBSERVABLE = pueden ser varios, VERIFICAR si hay que NORMALIZARLOS para que se puedan comparar con distintos INPUTS
# Opciones:
# Número de celdas vivas: La cantidad total de celdas vivas en el sistema en un momento dado.
# Densidad de Celdas Vivas: Es la proporción de celdas vivas en relación al total de celdas en el dominio. (Más sofisticado que el de arriba)
# Distancia promedio de celdas vivas al centro: La distancia promedio de todas las celdas vivas al centro del dominio.
# Radio del Patrón : Al igual que en la pregunta original, puedes medir la distancia de la celda viva más lejana al centro del dominio.

# Entropía: Puedes calcular la entropía del sistema para evaluar su nivel de desorden o complejidad. Una entropía alta podría indicar una gran diversidad de patrones.
# double p1 = (double) countAlive / totalCells;
#    double p0 = 1 - p1;
#
#    // Calcular entropía
#    double entropy = -p1 * Math.log(p1) / Math.log(2) - p0 * Math.log(p0) / Math.log(2);


# GRAFICOS PEDIDOS:
# 1) Animación (2d, 3d segun corresponda)
# 2) Observable vs Tiempo
# 3) Promedio y Desvio Estandar del Observable vs Input