import numpy as np

def ingresar_matriz(nombre):
    filas = int(input(f"Ingresa el número de filas de la matriz {nombre}: "))
    columnas = int(input(f"Ingresa el número de columnas de la matriz {nombre}: "))
    print(f"Introduce los elementos de la matriz {nombre} fila por fila, separados por espacios:")
    matriz = []
    for i in range(filas):
        fila = list(map(float, input(f"Fila {i+1}: ").split()))
        while len(fila) != columnas:
            print(f"❌ Debes ingresar exactamente {columnas} elementos")
            fila = list(map(float, input(f"Fila {i+1}: ").split()))
        matriz.append(fila)
    return np.array(matriz)

def mostrar_menu():
    print("\n--- Calculadora Matricial con NumPy ---")
    print("1. Suma de matrices")
    print("2. Resta de matrices")
    print("3. Multiplicación de matrices")
    print("4. Transposición de una matriz")
    print("5. Salir")
    opcion = input("Selecciona una opción: ")
    return opcion

def main():
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":  # Suma
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape == B.shape:
                print("\n✅ Resultado de la suma:\n", A + B)
            else:
                print("❌ Las matrices deben tener las mismas dimensiones para sumarse.")
        
        elif opcion == "2":  # Resta
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape == B.shape:
                print("\n✅ Resultado de la resta:\n", A - B)
            else:
                print("❌ Las matrices deben tener las mismas dimensiones para restarse.")
        
        elif opcion == "3":  # Multiplicación
            A = ingresar_matriz("A")
            B = ingresar_matriz("B")
            if A.shape[1] == B.shape[0]:
                print("\n✅ Resultado de la multiplicación:\n", np.dot(A, B))
            else:
                print("❌ El número de columnas de A debe coincidir con el número de filas de B.")
        
        elif opcion == "4":  # Transposición
            A = ingresar_matriz("A")
            print("\n✅ Transpuesta de la matriz:\n", A.T)
        
        elif opcion == "5":  # Salir
            print("👋 Saliendo de la calculadora matricial...")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
