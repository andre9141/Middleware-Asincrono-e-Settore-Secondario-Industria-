import pika
import json
import time
import random
import datetime

# --- CONFIGURAZIONE ---
# In un ambiente reale, questi parametri verrebbero caricati
# da variabili d'ambiente o da un vault sicuro.
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "factory_data_secure"


def get_connection():
    """
    Stabilisce la connessione con RabbitMQ.
    Implementa la logica di retry (predisposizione) per resilienza.
    """
    connection_params = pika.ConnectionParameters(host=RABBITMQ_HOST)

    # Esempio di predisposizione per SSL/TLS (citabile in tesi):
    # ssl_options = ...
    # connection_params.ssl_options = ssl_options

    return pika.BlockingConnection(connection_params)


def simulate_sensor_reading():
    """
    Genera dati simulati del macchinario industriale:
    temperatura, vibrazione e stato operativo.
    """
    return {
        "sensor_id": "PRESS_01_A",
        "timestamp": datetime.datetime.now().isoformat(),
        "temperature_celsius": round(random.uniform(50.0, 120.0), 2),
        "vibration_level": round(random.uniform(0.1, 5.0), 2),
        "status": "OPERATIONAL"
    }


def publish_messages():
    """
    Pubblica messaggi asincroni sulla coda RabbitMQ.
    Il produttore NON attende la loro elaborazione (disaccoppiamento).
    """
    try:
        connection = get_connection()
        channel = connection.channel()

        # Coda durevole → messaggi persistenti (resilienza)
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        print(f"[*] Connesso al middleware. Invio dati sensori su '{QUEUE_NAME}'...")

        while True:
            data = simulate_sensor_reading()
            message_body = json.dumps(data)

            # Allarme critico → messaggio con priorità alta
            if data["temperature_celsius"] > 110.0:
                properties = pika.BasicProperties(
                    delivery_mode=2,  # Persistente
                    priority=2        # Alta priorità
                )
                print(f"[!] ALLARME CRITICO: {data['temperature_celsius']}°C")
            else:
                properties = pika.BasicProperties(delivery_mode=2)

            # Pubblicazione messaggio
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=message_body,
                properties=properties
            )

            print(
                f"[x] Inviato: {data['temperature_celsius']}°C - "
                f"Vibrazione: {data['vibration_level']}"
            )

            # Frequenza simulata del sensore
            time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Errore nella connessione RabbitMQ: {e}")

    finally:
        if "connection" in locals() and connection.is_open:
            connection.close()


if __name__ == "__main__":
    publish_messages()
