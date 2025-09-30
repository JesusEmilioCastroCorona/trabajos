Este proyecto es un juego de consola inspirado en Pokémon, desarrollado en Python aplicando los principios de Programación Orientada a Objetos (POO).

El jugador puede:

Crear una partida y elegir un Pokémon inicial.

Moverse por un mapa en consola.

Encontrar Pokémon salvajes de forma aleatoria.

Iniciar combates por turnos utilizando movimientos.

Guardar y cargar partidas.

⚙️ Estructura General

El código se organiza en varias secciones principales:

Configuración y constantes

Mapas de emojis, tabla de efectividades de tipos, estadísticas de movimientos base.

Se definen reglas generales que el juego utiliza en los combates.

Clases principales de POO

Movimiento: Representa un ataque o habilidad.

Pokemon: Clase padre que define atributos y métodos comunes a todos los Pokémon.

Ignarok, BombardiloCocodrilo, Verdalis: Subclases (herencia) que personalizan Pokémon iniciales.

Otros Pokémon salvajes (Pidgey, Rattata, etc.) también heredan de Pokemon.

Juego: Clase principal que gestiona el flujo general del juego (mapa, menús, combates, guardado).

Persistencia

Se utiliza JSON para guardar/cargar partidas (guardar_partida y cargar_partida).

Sistema de Combate

Basado en turnos: el jugador elige un movimiento y luego el enemigo responde.

Se aplican modificadores como STAB (Same Type Attack Bonus), efectividad de tipos y variantes de ataque.

🧩 Conceptos de POO utilizados
1. Clases

Movimiento, Pokemon, Juego y cada Pokémon específico son clases que modelan elementos del juego.

Cada clase encapsula datos (atributos) y comportamientos (métodos).

2. Objetos e Instancias

Cada Pokémon creado en el juego (Ignarok(), Pidgey(), etc.) es una instancia de una clase.

Cada objeto mantiene sus propios valores (HP, ataque, movimientos).

3. Herencia

Ignarok, Verdalis y BombardiloCocodrilo heredan de Pokemon.

De esta forma, comparten atributos y métodos básicos (atacar, esta_derrotado), pero inicializan con estadísticas y habilidades distintas.

Polimorfismo

El método atacar() funciona de forma distinta dependiendo de:

El movimiento elegido (puede ser "Ataque doble", "Sin efecto", etc.).

El tipo de Pokémon enemigo, ya que se aplican multiplicadores de efectividad.

También se observa en el constructor de las clases hijas: cada Pokémon redefine su propia forma de inicializarse sin cambiar la lógica de combate.

5. Encapsulamiento

La información de cada Pokémon está contenida dentro del objeto (HP, ataque, movimientos).

El acceso y modificación de estos datos ocurre a través de métodos (atacar, esta_derrotado, etc.), en lugar de manipular atributos directamente desde fuera.

6. Abstracción

Se definen clases como Movimiento y Pokemon para representar conceptos generales del juego.

El jugador solo necesita interactuar con menús y comandos, mientras que la lógica interna del combate está abstraída en métodos.
