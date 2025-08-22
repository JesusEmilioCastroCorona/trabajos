def leer_estudiantes(nombre_archivo):
    """Lee estudiantes y calificaciones desde un archivo"""
    estudiantes = []
    try:
        with open(nombre_archivo, "r") as f:
            for linea in f:
                try:
                    nombre, calificacion = linea.strip().split(",")
                    estudiantes.append((nombre, float(calificacion)))
                except ValueError:
                    print(f"⚠ Error en formato de línea: {linea.strip()}")
    except FileNotFoundError:
        print(f"❌ El archivo {nombre_archivo} no existe.")
    return estudiantes


def calcular_promedio(estudiantes):
    """Calcula el promedio de calificaciones"""
    if not estudiantes:
        return 0
    total = sum(calificacion for _, calificacion in estudiantes)
    return total / len(estudiantes)


def generar_reporte(estudiantes, nombre_archivo_reporte):
    """Genera un archivo de reporte con el promedio"""
    promedio = calcular_promedio(estudiantes)
    try:
        with open(nombre_archivo_reporte, "w") as f:
            for nombre, calificacion in estudiantes:
                f.write(f"{nombre},{calificacion}\n")
            f.write(f"Promedio general: {promedio:.2f}\n")
        print(f"✅ Reporte generado en {nombre_archivo_reporte}")
    except Exception as e:
        print(f"❌ Error al generar el reporte: {e}")


def agregar_estudiante(nombre_archivo):
    """Permite al usuario agregar nuevos estudiantes al archivo"""
    try:
        with open(nombre_archivo, "a") as f:
            nombre = input("Ingrese el nombre del estudiante: ")
            calificacion = input("Ingrese la calificación: ")
            f.write(f"{nombre},{calificacion}\n")
        print("✅ Estudiante agregado correctamente.")
    except Exception as e:
        print(f"❌ Error al agregar estudiante: {e}")


def main():
    archivo_estudiantes = "estudiantes.txt"
    archivo_reporte = "reporte.txt"

    estudiantes = leer_estudiantes(archivo_estudiantes)

    if estudiantes:
        promedio = calcular_promedio(estudiantes)
        print(f"📊 Promedio general: {promedio:.2f}")

        generar_reporte(estudiantes, archivo_reporte)

    opcion = input("¿Desea agregar un nuevo estudiante? (s/n): ").lower()
    if opcion == "s":
        agregar_estudiante(archivo_estudiantes)


if __name__ == "__main__":
    main()
