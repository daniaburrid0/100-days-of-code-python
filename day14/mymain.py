# Actividad: Desarrollo del Juego "Higher Lower" en Python

# Objetivo:
# Crear un programa en Python que simule el juego "Higher Lower", donde los jugadores deben adivinar qué celebridad o entidad tiene más seguidores en redes sociales.

# Requisitos:

# 1. Utiliza los archivos proporcionados: `art.py` para el logo y el símbolo VS, y `game_data.py` que contiene la información de las celebridades.

# 2. Implementa las siguientes funciones:
#    - `profile()`: Para seleccionar aleatoriamente un perfil de la lista de datos y formatear su información.
#    - `higher_lower()`: Para ejecutar el juego principal.

# 3. El juego debe funcionar de la siguiente manera:
#    - Muestra dos perfiles aleatorios (A y B) al jugador.
#    - Pide al jugador que adivine cuál tiene más seguidores.
#    - Si el jugador acierta, aumenta su puntuación y continúa el juego con un nuevo perfil B.
#    - Si el jugador se equivoca, el juego termina y muestra la puntuación final.

# 4. Características adicionales:
#    - Muestra el logo del juego al inicio de cada ronda.
#    - Utiliza la función `clear()` de replit para limpiar la pantalla entre rondas.
#    - Asegúrate de que los perfiles A y B nunca sean iguales.
#    - Muestra la puntuación actual después de cada acierto.

# 5. Al finalizar el juego, pregunta al jugador si desea jugar de nuevo.

# 6. Maneja correctamente las entradas del usuario (a/b) y las comparaciones de seguidores.

# Sugerencias:
# - Utiliza bucles while para mantener el juego en ejecución mientras el jugador siga acertando.
# - Presta atención a la presentación de la información para que sea clara y atractiva.
# - Considera usar funciones auxiliares para hacer el código más modular y legible.

# Bonus:
# - Añade un sistema de récords para guardar la mejor puntuación.
# - Implementa diferentes niveles de dificultad (por ejemplo, mostrando menos información sobre los perfiles en niveles más difíciles).

# ¡Diviértete programando tu versión de "Higher Lower"!

# Actividad: Desarrollo del Juego "Higher Lower" en Python

# Objetivo:
# Crear un programa en Python que simule el juego "Higher Lower", donde los jugadores deben adivinar qué celebridad o entidad tiene más seguidores en redes sociales.

# Requisitos:

# 1. Utiliza los archivos proporcionados: `art.py` para el logo y el símbolo VS, y `game_data.py` que contiene la información de las celebridades.

# 2. Implementa las siguientes funciones:
#    - `profile()`: Para seleccionar aleatoriamente un perfil de la lista de datos y formatear su información.
#    - `higher_lower()`: Para ejecutar el juego principal.

# 3. El juego debe funcionar de la siguiente manera:
#    - Muestra dos perfiles aleatorios (A y B) al jugador.
#    - Pide al jugador que adivine cuál tiene más seguidores.
#    - Si el jugador acierta, aumenta su puntuación y continúa el juego con un nuevo perfil B.
#    - Si el jugador se equivoca, el juego termina y muestra la puntuación final.

# 4. Características adicionales:
#    - Muestra el logo del juego al inicio de cada ronda.
#    - Utiliza la función `clear()` de replit para limpiar la pantalla entre rondas.
#    - Asegúrate de que los perfiles A y B nunca sean iguales.
#    - Muestra la puntuación actual después de cada acierto.

# 5. Al finalizar el juego, pregunta al jugador si desea jugar de nuevo.

# 6. Maneja correctamente las entradas del usuario (a/b) y las comparaciones de seguidores.

# Sugerencias:
# - Utiliza bucles while para mantener el juego en ejecución mientras el jugador siga acertando.
# - Presta atención a la presentación de la información para que sea clara y atractiva.
# - Considera usar funciones auxiliares para hacer el código más modular y legible.

# Bonus:
# - Añade un sistema de récords para guardar la mejor puntuación.
# - Implementa diferentes niveles de dificultad (por ejemplo, mostrando menos información sobre los perfiles en niveles más difíciles).

# ¡Diviértete programando tu versión de "Higher Lower"!
import game_data, art
import random

def higher_lower():
    score = 0
    game_over = False
    profile_a = game_data.data[random.randint(0, len(game_data.data) - 1)]
    profile_b = game_data.data[random.randint(0, len(game_data.data) - 1)]

    while profile_a == profile_b:
        profile_b = game_data.data[random.randint(0, len(game_data.data) - 1)]

    while not game_over:
        print(f"Compara A: {profile_a['name']}, un {profile_a['description']}, de {profile_a['country']}.")
        print(art.vs)
        print(f"Contra B: {profile_b['name']}, un {profile_b['description']}, de {profile_b['country']}.")

        guess = input("¿Quién tiene más seguidores? Escribe 'A' o 'B': ").upper()

        if (guess == 'A' and profile_a['follower_count'] > profile_b['follower_count']) or \
           (guess == 'B' and profile_b['follower_count'] > profile_a['follower_count']):
            score += 1
            print(f"¡Correcto! Puntuación actual: {score}")
            profile_a = profile_b
            profile_b = game_data.data[random.randint(0, len(game_data.data) - 1)]
            while profile_a == profile_b:
                profile_b = game_data.data[random.randint(0, len(game_data.data) - 1)]
        else:
            game_over = True
            print(f"Lo siento, eso es incorrecto. Puntuación final: {score}")

def comenzar_juego():
    print(art.logo)
    higher_lower()

def main():
    print("¿Comenzamos con el juego? (Sí/No)")
    while True:
        respuesta = input().lower()
        if respuesta in ['si', 'sí', 'no', 's', 'n']:
            break
        else:
            print("Por favor, ingrese 'Sí' o 'No'.")
    respuesta = input().lower()
    if respuesta == 'si' or respuesta == 'sí':
        print("¡Genial! Empecemos.")
        comenzar_juego()
    else:
        print("De acuerdo, hasta luego.")
        return

if __name__ == "__main__":
    main()
