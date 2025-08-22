import libreria1
import libreria2
import libreria3

def menu():
    print("\n=== Gestor de Utilidades ===")
    print("1. Calculadora")
    print("2. Arte ASCII")
    print("3. Corrector de texto")
    print("4. Salir")

while True:
    menu()
    opcion = input("Elige una opción: ")

    if opcion == "1":
        a = int(input("Ingresa número A: "))
        b = int(input("Ingresa número B: "))
        print("Suma:", libreria1.suma(a, b))
        print("Resta:", libreria1.resta(a, b))
        print("Multiplicación:", libreria1.multiplicacion(a, b))
        print("División:", libreria1.division(a, b))

    elif opcion == "2":
        print(libreria2.banner("Bienvenido"))
        print(libreria2.corazon())

    elif opcion == "3":
        texto = input("Escribe un texto: ")
        print("Texto corregido:", libreria3.corrector(texto))

    elif opcion == "4":
        print("Saliendo...")
        break

    else:
        print("Opción inválida, intenta otra vez.")
