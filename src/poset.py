import numpy as np 

class Poset_finito:
    def __init__(self, tamaño, relaciones):
        """
        tamaño: Número de puntos en el poset
        relaciones: lista de tuplas
        """

        self.tamaño = tamaño
        self.adyacencia = np.zeros((tamaño, tamaño), dtype=int) # matriz de adyacencia

        for a,b in relaciones:
            if (a >= tamaño) or (b >= tamaño):
                raise ValueError("Índice fuera de rango")
            self.adyacencia[a,b] = 1
        
        # Hacer la relación reflexiva
        self.hacer_reflexivo()
        
        # Calcular clausura transitiva
        self.adyacencia = self.clausura_transitiva()
        
        # Verificar propiedades básicas del poset
        if not self.es_antisimetrico():
            raise ValueError("Las relaciones no son antisimétricas")
    
    def es_antisimetrico(self):
        """
        Verifica que si a <= b y b <= a entonces a = b
        """
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                if i != j and self.adyacencia[i,j] == 1 and self.adyacencia[j,i] == 1:
                    return False
        return True
    
    def es_transitivo(self):
        """
        Verifica que si a <= b y b <= c entonces a <= c
        """
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                for k in range(self.tamaño):
                    if self.adyacencia[i,j] == 1 and self.adyacencia[j,k] == 1:
                        if self.adyacencia[i,k] != 1:
                            return False
        return True
    
    def clausura_transitiva(self):
        """
        Calcula la clausura transitiva usando el algoritmo de Warshall
        """
        clausura = self.adyacencia.copy()
        
        for k in range(self.tamaño):
            for i in range(self.tamaño):
                for j in range(self.tamaño):
                    clausura[i,j] = clausura[i,j] or (clausura[i,k] and clausura[k,j])
        
        return clausura
    
    def es_reflexivo(self):
        """
        Verifica que a <= a para todo a
        """
        for i in range(self.tamaño):
            if self.adyacencia[i,i] != 1:
                return False
        return True
    
    def hacer_reflexivo(self):
        """
        Hace la relación reflexiva añadiendo a <= a para todo a
        """
        for i in range(self.tamaño):
            self.adyacencia[i,i] = 1
    
    def comparar_elementos(self, a, b):
        """
        Compara dos elementos: returns 1 si a < b, -1 si b < a, 0 si incomparables
        """
        if a >= self.tamaño or b >= self.tamaño:
            raise ValueError("Índice fuera de rango")
        
        if self.adyacencia[a,b] == 1 and self.adyacencia[b,a] == 0:
            return 1  # a < b
        elif self.adyacencia[b,a] == 1 and self.adyacencia[a,b] == 0:
            return -1  # b < a
        elif a == b:
            return 0  # iguales
        else:
            return 0  # incomparables
    
    def obtener_cubiertos(self, elemento):
        """
        Retorna los elementos que cubren inmediatamente a elemento
        """
        if elemento >= self.tamaño:
            raise ValueError("Índice fuera de rango")
        
        cubiertos = []
        for j in range(self.tamaño):
            if self.adyacencia[elemento,j] == 1:  # elemento <= j
                # Verificar si no hay k tal que elemento <= k <= j con k ≠ elemento,j
                es_cubierta = True
                for k in range(self.tamaño):
                    if k != elemento and k != j:
                        if self.adyacencia[elemento,k] == 1 and self.adyacencia[k,j] == 1:
                            es_cubierta = False
                            break
                if es_cubierta and j != elemento:
                    cubiertos.append(j)
        
        return cubiertos
    
    def obtener_cubiertos_inferiores(self, elemento):
        """
        Retorna los elementos que son cubiertos inmediatamente por elemento
        """
        if elemento >= self.tamaño:
            raise ValueError("Índice fuera de rango")
        
        cubiertos_inf = []
        for i in range(self.tamaño):
            if self.adyacencia[i,elemento] == 1:  # i <= elemento
                # Verificar si no hay k tal que i <= k <= elemento con k ≠ i,elemento
                es_cubierta_inf = True
                for k in range(self.tamaño):
                    if k != i and k != elemento:
                        if self.adyacencia[i,k] == 1 and self.adyacencia[k,elemento] == 1:
                            es_cubierta_inf = False
                            break
                if es_cubierta_inf and i != elemento:
                    cubiertos_inf.append(i)
        
        return cubiertos_inf
    
    def es_poset_valido(self):
        """
        Verifica todas las propiedades de un poset: reflexividad, antisimetría, transitividad
        """
        return self.es_reflexivo() and self.es_antisimetrico() and self.es_transitivo()
    
    def __str__(self):
        """
        Representación en cadena del poset
        """
        resultado = f"Poset con {self.tamaño} elementos:\n"
        resultado += "Matriz de adyacencia:\n"
        for i in range(self.tamaño):
            fila = ""
            for j in range(self.tamaño):
                fila += str(self.adyacencia[i,j]) + " "
            resultado += fila + "\n"
        return resultado