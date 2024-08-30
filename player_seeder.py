import requests
import random
from datetime import datetime, timedelta

# Configuración
base_url = "http://localhost:8000/api/v1/games/data"
school_code = "SCH001"  # Cambia este código de escuela según sea necesario
stages = ["R0", "R1", "R2", "R3", "R4"]
names = ["michael", "sarah", "luke", "emily", "daniel", "olivia", "joshua", "isabella"]
estado_choices = ["completado", "abandonado"]

# Función para generar una fecha aleatoria
def generate_random_time(start_time, end_time):
    time_diff = end_time - start_time
    random_diff = random.randint(0, int(time_diff.total_seconds()))
    return start_time + timedelta(seconds=random_diff)

# Generar datos para un niño
def generate_game_session_data():
    stage = random.choice(stages)
    player_name = f"{school_code}-{stage}-{random.choice(names)}"
    start_time = datetime(2024, 7, 8, 19, 18, 0)
    end_time = start_time + timedelta(minutes=random.randint(1, 10))
    
    # JSON tipo "jugador"
    jugador_data = {
        "tipo": "jugador",
        "avatar": "mestizo-h",
        "id_registro": player_name,
        "nombre_juego": "NamiNam1",
        "fecha_inicio_saludo": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_inicio_nombre": (start_time + timedelta(seconds=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_fin_nombre": (start_time + timedelta(seconds=6)).strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_inicio_creditos": "",
        "fecha_fin_creditos": ""
    }
    
    # JSON tipo "historia"
    historia_data = {
        "tipo": "historia",
        "id_registro": player_name,
        "nombre_juego": "NamiNam1",
        "descripcion_juego": "Alimentos Saludables en Lonchera",
        "nombre_capitulo": "Identificacion Alimentos",
        "descripcion_capitulo": "Ñami Ñam necesita de ayuda de los niños para recolectar alimentos saludables y deshechar no saludables",
        "nombre_historia": "Identificacion Alimentos en Lonchera",
        "fecha_inicio": (start_time + timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_fin": (start_time + timedelta(minutes=2, seconds=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "tiempo_juego": "5",
        "estado": random.choice(estado_choices),
        "descripcion_historia": "Ñami Ñam necesita de ayuda de los niños para disfrutar de los alimentos saludables",
        "duracion": str(random.randint(20, 40))
    }
    
    # JSON tipo "juego"
    juego_data = {
        "tipo": "juego",
        "id_registro": player_name,
        "nombre_juego": "NamiNam1",
        "descripcion_juego": "Alimentos Saludables en Lonchera",
        "nombre_capitulo": "Identificacion Alimentos",
        "descripcion_capitulo": "Ñami Ñam necesita de ayuda de los niños para disfrutar de los alimentos saludables",
        "nombre_historia": "Identificacion Alimentos en Lonchera",
        "fecha_inicio": (start_time + timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_fin": (start_time + timedelta(minutes=3, seconds=11)).strftime("%Y-%m-%d %H:%M:%S"),
        "tiempo_juego": "11",
        "estado": random.choice(estado_choices),
        "nombre_nivel": "Lonchera Básica Activity 1",
        "descripcion_nivel": "Captura alimentos saludable - Lento",
        "correctas": str(random.randint(0, 5)),
        "incorrectas": str(random.randint(0, 2))
    }
    
    return [jugador_data, historia_data, juego_data]

# Enviar los datos al servidor
def send_data(data):
    for item in data:
        response = requests.post(base_url, json=item)
        if response.status_code == 200:
            print(f"Data sent successfully: {item['tipo']}")
        else:
            print(f"Failed to send data: {response.status_code} - {response.text}")

# Ejecutar la generación y envío de datos
if __name__ == "__main__":
    session_data = generate_game_session_data()
    send_data(session_data)
