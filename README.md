# Trabajo Práctico: Clon de Pac-Man en Pygame

¡Bienvenido al desarrollo de **Pac-Man**! Este proyecto es un videojuego en 2D desarrollado en Python utilizando la biblioteca **Pygame**. Recrea las mecánicas clásicas del arcade original de los años 80, incluyendo el movimiento del personaje, la recolección de puntos (pellets) y un sistema avanzado de inteligencia artificial para el comportamiento dinámico de los fantasmas.

---

## 🚀 Características del Juego

* **Inteligencia Artificial Clásica:** Los fantasmas cuentan con 3 modos lógicos de comportamiento automatizado:
    * **Chase (Persecución):** Buscan activamente la posición de Pac-Man en el mapa de forma coordinada.
    * **Scatter (Dispersión):** Se retiran temporalmente a patrullar sus respectivas esquinas del laberinto.
    * **Frightened (Asustado):** Al comer un Power Pellet, los fantasmas se tornan azules, se mueven de forma errática a menor velocidad y parpadean (alternando a blanco) en los últimos 2 segundos como advertencia.
* **Ciclo de Vida de los Fantasmas:** Al ser devorados por Pac-Man, se convierten en ojos dinámicos orientados hacia su dirección de movimiento que viajan de regreso a la *Ghost House* para regenerarse.
* **Sistema de Vidas y Reseteo:** Pac-Man cuenta con un contador de vidas y un sistema de control de salida por conteo de bolitas consumidas que regula qué fantasmas pueden abandonar la base de forma progresiva.
* **Efectos de Sonido:** Totalmente integrado con audios arcade para la muerte, el consumo de puntos y los estados especiales.

---