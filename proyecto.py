import json
import random
from colorama import Fore, Style, init

init(autoreset=True)

def cargar_jugadores():
    try:
        with open("jugadores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_jugadores(jugadores):
    with open("jugadores.json", "w") as f:
        json.dump(jugadores, f, indent=4)

def registrar_jugador(jugadores):
    nombre = input("Nombre del jugador: ")
    print("Elige clase: 1) Guerrero 2) Mago 3) Explorador")
    eleccion = input("> ")

    clases = {"1": "Guerrero", "2": "Mago", "3": "Explorador"}
    clase = clases.get(eleccion, "Aventurero")

    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "vida": 30,
        "inventario": {"pociones": 2}
    }
    jugadores[nombre] = jugador
    guardar_jugadores(jugadores)
    print(Fore.GREEN + f"¡Bienvenido, {nombre} el {clase}!")
    return jugador

def cargar_jugador(jugadores):
    if not jugadores:
        print(Fore.RED + "No hay jugadores registrados.")
        return None
    print("Jugadores disponibles:")
    for nombre in jugadores:
        print("-", nombre)
    nombre = input("Elige jugador: ")
    return jugadores.get(nombre)

def aventura(jugador):
    print(Style.BRIGHT + "\nTu aventura comienza en una aldea misteriosa...")
    print("Te acercas a una bifurcación en el bosque.")
    decision = input("A) Ir por el camino oscuro\nB) Tomar el sendero iluminado\n> ").upper()

    if decision == "A":
        print("Te adentras en la oscuridad... ¡un goblin aparece!")
        combate(jugador, {"nombre": "Goblin", "vida": 10, "ataque": 3})
    else:
        print("El sendero iluminado parece tranquilo... pero escuchas ruidos extraños.")
        combate(jugador, {"nombre": "Lobo", "vida": 12, "ataque": 4})

def combate(jugador, enemigo):
    print(Fore.RED + f"\nCombate: ¡Un {enemigo['nombre']} te ataca!")
    vida_jugador = jugador["vida"]
    vida_enemigo = enemigo["vida"]

    while vida_jugador > 0 and vida_enemigo > 0:
        print(f"\nTu vida: {vida_jugador} | Vida del {enemigo['nombre']}: {vida_enemigo}")
        accion = input("¿Atacar (A) o usar poción (P)? ").upper()

        if accion == "A":
            daño = random.randint(3, 8)
            vida_enemigo -= daño
            print(Fore.CYAN + f"Atacas y haces {daño} de daño.")
        elif accion == "P" and jugador["inventario"].get("pociones", 0) > 0:
            vida_jugador += 10
            jugador["inventario"]["pociones"] -= 1
            print(Fore.GREEN + f"Usas una poción. Vida restaurada a {vida_jugador}.")
        else:
            print("¡Acción inválida!")

        if vida_enemigo > 0:
            daño_enemigo = random.randint(1, enemigo["ataque"])
            vida_jugador -= daño_enemigo
            print(Fore.RED + f"El {enemigo['nombre']} te golpea por {daño_enemigo}.")

    if vida_jugador > 0:
        print(Fore.YELLOW + f"\n¡Has derrotado al {enemigo['nombre']}!")
        jugador["nivel"] += 1
        print(Fore.MAGENTA + f"¡Subes a nivel {jugador['nivel']}!")
    else:
        print(Fore.RED + "\nHas sido derrotado...")

def main():
    jugadores = cargar_jugadores()
    print("Bienvenido al mundo de PyRPG")
    print("1. Registrar nuevo jugador")
    print("2. Cargar jugador existente")
    opcion = input("> ")

    if opcion == "1":
        jugador = registrar_jugador(jugadores)
    else:
        jugador = cargar_jugador(jugadores)
        if not jugador:
            return

    aventura(jugador)
    jugadores[jugador["nombre"]] = jugador
    guardar_jugadores(jugadores)

if __name__ == "__main__":
    main()
