estudiantes = {}

def agregar_estudiante():
    id_est = input("Ingrese el ID del estudiante (ej. A001): ")
    if id_est in estudiantes:
        print("❌ Error: Ya existe un estudiante con ese ID.")
        return
    
    nombre = input("Ingrese el nombre completo: ")
    try:
        edad = int(input("Ingrese la edad: "))
    except ValueError:
        print("❌ Error: La edad debe ser un número entero.")
        return
    
    calificaciones = []
    while True:
        cal = input("Ingrese una calificación (o 'fin' para terminar): ")
        if cal.lower() == "fin":
            break
        try:
            cal = float(cal)
            calificaciones.append(cal)
        except ValueError:
            print("⚠️ Ingrese un número válido para la calificación.")
    
    estudiantes[id_est] = {"nombre": nombre, "edad": edad, "calificaciones": calificaciones}
    print(f"✅ Estudiante {id_est} agregado correctamente.")


def mostrar_estudiantes():
    if not estudiantes:
        print("📭 No hay estudiantes registrados.")
        return
    for id_est, datos in estudiantes.items():
        print(f"{id_est} - {datos['nombre']} - Edad: {datos['edad']} - Calificaciones: {datos['calificaciones']}")


def calcular_promedio():
    id_est = input("Ingrese el ID del estudiante: ")
    if id_est not in estudiantes:
        print("❌ Error: No existe un estudiante con ese ID.")
        return
    notas = estudiantes[id_est]["calificaciones"]
    if notas:
        promedio = sum(notas) / len(notas)
        print(f"📊 Estudiante {id_est} - {estudiantes[id_est]['nombre']} - Promedio: {promedio:.2f}")
    else:
        print("⚠️ El estudiante no tiene calificaciones registradas.")


def eliminar_estudiante():
    id_est = input("Ingrese el ID del estudiante a eliminar: ")
    if id_est in estudiantes:
        del estudiantes[id_est]
        print(f"🗑️ Estudiante {id_est} eliminado correctamente.")
    else:
        print("❌ Error: No existe un estudiante con ese ID.")


def menu():
    while True:
        print("\n--- Menú de Gestión de Estudiantes ---")
        print("1. Agregar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Calcular promedio de un estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            mostrar_estudiantes()
        elif opcion == "3":
            calcular_promedio()
        elif opcion == "4":
            eliminar_estudiante()
        elif opcion == "5":
            print("👋 Saliendo del programa...")
            break
        else:
            print("⚠️ Opción no válida, intente de nuevo.")

menu()
