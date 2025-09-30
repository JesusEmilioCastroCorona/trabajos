import os
import time
import random
import json


def cls():
    """Limpia la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

PLAYER_ICON = '👤'
GRASS_ICON = '🌿'
MAP_WIDTH = 20
MAP_HEIGHT = 10

EFFECTIVENESS_TABLE = {
    'Infierno': {'Flora': 2.0, 'Marea': 0.5, 'Infierno': 1.0, 'Normal': 1.0},
    'Marea': {'Infierno': 2.0, 'Flora': 0.5, 'Marea': 1.0, 'Normal': 1.0},
    'Flora': {'Marea': 2.0, 'Infierno': 0.5, 'Flora': 1.0, 'Normal': 1.0},
    'Normal': {'Infierno': 1.0, 'Marea': 1.0, 'Flora': 1.0, 'Normal': 1.0},
}

MOVEMENT_BASE_STATS = {
    'Placaje': {'poder': 40, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Ascuas': {'poder': 40, 'tipo': 'Infierno', 'variante': 'Ataque básico'},
    'Pistola Agua': {'poder': 40, 'tipo': 'Marea', 'variante': 'Ataque básico'},
    'Latigo Cepa': {'poder': 45, 'tipo': 'Flora', 'variante': 'Ataque básico'},
    'Ataque Rapido': {'poder': 40, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Furia Dragon': {'poder': 60, 'tipo': 'Normal', 'variante': 'Ataque doble'},
    'Burbuja': {'poder': 20, 'tipo': 'Marea', 'variante': 'Ataque doble'},
    'Viento Plata': {'poder': 60, 'tipo': 'Normal', 'variante': 'Ataque básico'},
    'Bostezo': {'poder': 0, 'tipo': 'Normal', 'variante': 'Ataque pierde turno'},
    'Salpicadura': {'poder': 0, 'tipo': 'Normal', 'variante': 'Sin efecto'},
}


class Movimiento:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo
        stats = MOVEMENT_BASE_STATS.get(nombre, {})
        self.variante = stats.get('variante', 'Ataque básico')
        if nombre not in MOVEMENT_BASE_STATS:
            MOVEMENT_BASE_STATS[nombre] = {'poder': poder, 'tipo': tipo, 'variante': self.variante}

    def atacar(self):
        if self.variante == 'Ataque doble':
            print(f"[{self.nombre}] - ¡Doble impacto!")
            return 2 
        elif self.variante == 'Sin efecto':
            print(f"[{self.nombre}] - ¡No tuvo efecto!")
            return 0
        elif self.variante == 'Ataque pierde turno':
            print(f"[{self.nombre}] - ¡Necesita recargar!")
            return 1
        else:
            return 1

    def __str__(self):
        return f"{self.nombre} ({self.tipo} | Pwr: {self.poder} | Var: {self.variante})"

class Pokemon:
    def __init__(self, arte_ascii, nombre, tipo, ataque, defensa, hp_max, habilidad, movimientos_nombres):
        self.arte_ascii = arte_ascii
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.hp_max = hp_max
        self.hp_actual = hp_max
        self.habilidad_nombre = habilidad
        self.movimientos = []
        for nombre in movimientos_nombres:
            stats = MOVEMENT_BASE_STATS.get(nombre)
            if stats:
                self.movimientos.append(Movimiento(nombre, stats['poder'], stats['tipo']))

    def atacar(self, movimiento_obj, objetivo, tabla_tipos):
        variante_multi = movimiento_obj.atacar()
        if variante_multi == 0:
            return 0 

        damage_pre_mod = ((((self.ataque * movimiento_obj.poder) / objetivo.defensa) / 10) + 1)
        stab = 1.5 if self.tipo == movimiento_obj.tipo else 1.0
        efectividad = tabla_tipos.get(movimiento_obj.tipo, {}).get(objetivo.tipo, 1.0)
        final_damage = int(damage_pre_mod * stab * efectividad * variante_multi)
        
        objetivo.hp_actual = max(0, objetivo.hp_actual - final_damage)
        
        if efectividad > 1.0:
            print("¡Es SÚPER EFICAZ!")
        elif efectividad < 1.0 and efectividad > 0:
            print("No es muy eficaz...")
        elif efectividad == 0:
            print("¡No tiene efecto!")
        return final_damage

    def habilidad(self):
        return self.habilidad_nombre

    def esta_derrotado(self):
        return self.hp_actual <= 0
    
    def to_dict(self):
        return {
            'clase': self.__class__.__name__,
            'arte_ascii': self.arte_ascii,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'ataque': self.ataque,
            'defensa': self.defensa,
            'hp_max': self.hp_max,
            'hp_actual': self.hp_actual,
            'habilidad_nombre': self.habilidad_nombre,
            'movimientos_nombres': [m.nombre for m in self.movimientos]
        }
    
    @staticmethod
    def from_dict(data):
        cls_name = data['clase']
        if cls_name in globals() and issubclass(globals()[cls_name], Pokemon):
            cls_obj = globals()[cls_name]
            instance = cls_obj.__new__(cls_obj)
            instance.arte_ascii = data.get('arte_ascii', '❓') 
            instance.nombre = data['nombre']
            instance.tipo = data['tipo']
            instance.ataque = data['ataque']
            instance.defensa = data['defensa']
            instance.hp_max = data['hp_max']
            instance.hp_actual = data['hp_actual']
            instance.habilidad_nombre = data['habilidad_nombre']
            instance.movimientos = []
            for nombre in data['movimientos_nombres']:
                 stats = MOVEMENT_BASE_STATS.get(nombre)
                 if stats:
                    instance.movimientos.append(Movimiento(nombre, stats['poder'], stats['tipo']))
                 else:
                    instance.movimientos.append(Movimiento(nombre, 40, 'Normal'))
            return instance
        return None

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - HP: {self.hp_actual}/{self.hp_max}"


class Ignarok(Pokemon):  
    def __init__(self, nivel=5):
        hp = random.randint(39, 45)
        super().__init__(
            arte_ascii='🔥', nombre='Ignarok', tipo='Infierno',
            ataque=random.randint(52, 60), defensa=random.randint(43, 50),
            hp_max=hp, habilidad='Mar Llamas', movimientos_nombres=['Ascuas', 'Placaje']
        )

class BombardiloCocodrilo(Pokemon):  
    def __init__(self, nivel=5):
        hp = random.randint(44, 50)
        super().__init__(
            arte_ascii='💧', nombre='Bombardilo Cocodrilo', tipo='Marea',
            ataque=random.randint(48, 55), defensa=random.randint(65, 72),
            hp_max=hp, habilidad='Torrente', movimientos_nombres=['Pistola Agua', 'Placaje']
        )

class Verdalis(Pokemon):  
    def __init__(self, nivel=5):
        hp = random.randint(45, 49)
        super().__init__(
            arte_ascii='🌱', nombre='Verdalis', tipo='Flora',
            ataque=random.randint(49, 55), defensa=random.randint(49, 55),
            hp_max=hp, habilidad='Espesura', movimientos_nombres=['Latigo Cepa', 'Placaje']
        )


class Pidgey(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(40, 45)
        super().__init__('🦅', 'Pidgey', 'Normal', random.randint(45, 50),
                         random.randint(40, 45), hp, 'Tumbos', ['Ataque Rapido', 'Placaje'])

class Rattata(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(30, 35)
        super().__init__('🐀', 'Rattata', 'Normal', random.randint(56, 60),
                         random.randint(35, 40), hp, 'Fuga', ['Furia Dragon', 'Placaje'])

class Growlithe(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(55, 60)
        super().__init__('🐕', 'Growlithe', 'Infierno', random.randint(70, 75),
                         random.randint(45, 50), hp, 'Intimidación', ['Ascuas', 'Ataque Rapido'])

class Poliwag(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(40, 45)
        super().__init__('🐸', 'Poliwag', 'Marea', random.randint(50, 55),
                         random.randint(40, 45), hp, 'Humedad', ['Pistola Agua', 'Burbuja'])

class Oddish(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(45, 50)
        super().__init__('🍄', 'Oddish', 'Flora', random.randint(50, 55),
                         random.randint(50, 55), hp, 'Clorofila', ['Latigo Cepa', 'Burbuja'])

class Ponyta(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(50, 55)
        super().__init__('🐎', 'Ponyta', 'Infierno', random.randint(75, 80),
                         random.randint(45, 50), hp, 'Fuga', ['Ascuas', 'Viento Plata'])

class Goldeen(Pokemon):
    def __init__(self, nivel=5):
        hp = random.randint(45, 50)
        super().__init__('🐟', 'Goldeen', 'Marea', random.randint(67, 72),
                         random.randint(60, 65), hp, 'Nado Rápido', ['Pistola Agua', 'Viento Plata'])

WILD_POKEMON_CLASSES = [Pidgey, Rattata, Growlithe, Poliwag, Oddish, Ponyta, Goldeen]


class Juego:
    def __init__(self):
        self.partida_actual = self.default_partida_data()
        self.mapa = self.generar_mapa()
        self.efectividades = EFFECTIVENESS_TABLE

    def default_partida_data(self):
        return {
            'nombre_jugador': '',
            'equipo': [],
            'posicion_mapa': (int(MAP_WIDTH/2), int(MAP_HEIGHT/2)),
            'historial_combates': [],
            'pokemones_disponibles': ['Ignarok', 'BombardiloCocodrilo', 'Verdalis']
        }

    def guardar_partida(self):
        if not self.partida_actual['nombre_jugador']: return
        data_to_save = self.partida_actual.copy()
        data_to_save['equipo'] = [p.to_dict() for p in self.partida_actual['equipo']]
        with open(f"{self.partida_actual['nombre_jugador']}_partida.txt", 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def cargar_partida(self, nombre_partida=''):
        cls()
        if not nombre_partida:
             nombre_partida = input("Ingrese el nombre de la partida a cargar (Jugador): ").strip()
             if not nombre_partida: return False
        filename = f"{nombre_partida}_partida.txt"
        try:
            with open(filename, 'r') as f:
                data_loaded = json.load(f)
            equipo_cargado = [Pokemon.from_dict(p) for p in data_loaded['equipo'] if Pokemon.from_dict(p)]
            self.partida_actual = data_loaded
            self.partida_actual['equipo'] = equipo_cargado
            print(f"Partida de {nombre_partida} cargada con éxito.")
            time.sleep(1)
            return True
        except:
            print(f"No se pudo cargar la partida '{nombre_partida}'.")
            time.sleep(1.5)
            return False

    def menu_principal(self):
        while True:
            cls()
            print("=== MENÚ PRINCIPAL ===")
            print("1. Crear partida")
            print("2. Continuar partida")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == '1':
                self.menu_creacion()
                if self.partida_actual['nombre_jugador']:
                    self.mostrar_mapa()
            elif opcion == '2':
                if self.cargar_partida():
                    self.mostrar_mapa()
            elif opcion == '3':
                cls()
                print("¡Gracias por jugar!")
                break

    def menu_creacion(self):
        cls()
        nombre = input("Ingrese el nombre del jugador: ").strip()
        if not nombre: return
        self.partida_actual = self.default_partida_data()
        self.partida_actual['nombre_jugador'] = nombre
        print("\n--- ELIGE TU POKÉMON INICIAL ---")
        pokemones = self.partida_actual['pokemones_disponibles']
        for i, p_name in enumerate(pokemones):
            poke_class = globals().get(p_name)
            if poke_class:
                temp_poke = poke_class()
                print(f"{i+1}. {p_name} {temp_poke.arte_ascii}")
        while True:
            eleccion = input("Seleccione el número de su Pokémon inicial: ")
            try:
                index = int(eleccion) - 1
                if 0 <= index < len(pokemones):
                    poke_name = pokemones[index]
                    inicial = eval(f"{poke_name}()")
                    self.partida_actual['equipo'].append(inicial)
                    print(f"\n¡{nombre} ha elegido a {inicial.nombre}! ¡A la aventura!")
                    time.sleep(2)
                    self.guardar_partida()
                    break
            except:
                print("Entrada no válida.")

    def menu_estados(self, pokemon_target=None):
        cls()
        if not self.partida_actual['equipo']:
            print("El equipo está vacío.")
            time.sleep(1)
            return
        p = pokemon_target or self.partida_actual['equipo'][0]
        print(f"\nArte ASCII: {p.arte_ascii}")
        print(f"Nombre: {p.nombre}")
        print(f"Tipo: {p.tipo}")
        print(f"HP: {p.hp_actual}/{p.hp_max}")
        print(f"Ataque: {p.ataque} | Defensa: {p.defensa}")
        print(f"Habilidad: {p.habilidad_nombre}")
        print("Movimientos:")
        for mov in p.movimientos:
            print(f"  - {mov}")
        input("\nEnter para continuar...")

    def generar_mapa(self):
        return [[GRASS_ICON for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    def dibujar_mapa(self):
        cls()
        x, y = self.partida_actual['posicion_mapa']
        display_map = [row[:] for row in self.mapa]
        display_map[y][x] = PLAYER_ICON
        print("╔" + "═" * (MAP_WIDTH * 2 + 1) + "╗")
        for row in display_map:
            print("║ " + " ".join(row) + " ║")
        print("╚" + "═" * (MAP_WIDTH * 2 + 1) + "╝")
        print("\n|WASD-Mover | M-Menu | V-Volver")

    def gestionar_movimiento(self, tecla):
        x, y = self.partida_actual['posicion_mapa']
        new_x, new_y = x, y
        if tecla == 'w' and y > 0: new_y -= 1
        elif tecla == 's' and y < MAP_HEIGHT-1: new_y += 1
        elif tecla == 'a' and x > 0: new_x -= 1
        elif tecla == 'd' and x < MAP_WIDTH-1: new_x += 1
        elif tecla == 'm': self.menu_estados()
        elif tecla == 'v': 
            self.guardar_partida()
            return 'VOLVER'
        if (new_x, new_y) != (x, y):
            self.partida_actual['posicion_mapa'] = (new_x, new_y)
            if random.random() < 0.05:
                print("\n¡Un Pokémon salvaje apareció!")
                time.sleep(1)
                self.iniciar_combate()

    def mostrar_mapa(self):
        while True:
            self.dibujar_mapa()
            comando = input("> ").lower().strip()
            resultado = self.gestionar_movimiento(comando)
            if resultado == 'VOLVER':
                break

    # --- Combate ---
    def iniciar_combate(self):
        enemigo_class = random.choice(WILD_POKEMON_CLASSES)
        enemigo = enemigo_class()
        aliado = self.partida_actual['equipo'][0]
        print(f"\n¡Un {enemigo.nombre} salvaje apareció!")
        time.sleep(1)
        while not enemigo.esta_derrotado() and not aliado.esta_derrotado():
            cls()
            print(f"Tu {aliado.nombre}: {aliado.hp_actual}/{aliado.hp_max} HP")
            print(f"Enemigo {enemigo.nombre}: {enemigo.hp_actual}/{enemigo.hp_max} HP")
            print("\nMovimientos:")
            for i, mov in enumerate(aliado.movimientos):
                print(f"{i+1}. {mov}")
            eleccion = input("Elige un movimiento: ").strip()
            try:
                mov_sel = aliado.movimientos[int(eleccion)-1]
                daño = aliado.atacar(mov_sel, enemigo, self.efectividades)
                print(f"{aliado.nombre} usó {mov_sel.nombre}. Daño: {daño}")
            except:
                print("Entrada no válida.")
                continue
            time.sleep(1)
            if enemigo.esta_derrotado():
                print(f"¡{enemigo.nombre} fue derrotado!")
                break
            mov_enem = random.choice(enemigo.movimientos)
            daño = enemigo.atacar(mov_enem, aliado, self.efectividades)
            print(f"El enemigo {enemigo.nombre} usó {mov_enem.nombre}. Daño: {daño}")
            time.sleep(1)
        if aliado.esta_derrotado():
            print("Tu Pokémon fue derrotado... regresando al centro Pokémon.")
            aliado.hp_actual = aliado.hp_max
            time.sleep(2)

# --- Ejecución ---
if __name__ == "__main__":
    juego = Juego()
    juego.menu_principal()