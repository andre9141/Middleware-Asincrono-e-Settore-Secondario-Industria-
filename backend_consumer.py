import pika
import json
import time

# --- CONFIGURAZIONE ---
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "factory_data_secure"


def process_data(ch, method, properties, body):
    """
    Callback eseguita automaticamente ad ogni messaggio ricevuto
    dal middleware RabbitMQ.
    """
    payload = json.loads(body)

    # Simulazione elaborazione dati
    print(f" [>>] Ricevuto da {payload['sensor_id']}: Temp={payload['temperature_celsius']}°C")

    # Controllo anomalie (Security & Safety)
    if payload["temperature_celsius"] > 110.0:
        print(
            f"      [SECURITY ALERT] Temperatura critica! "
            f"Avvio protocollo di sicurezza per {payload['sensor_id']}"
        )
        # Qui potresti richiamare servizi esterni, inviare email/SMS, ecc.

    # ACK → conferma a RabbitMQ che il messaggio è stato elaborato correttamente
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Simula tempo di elaborazione
    time.sleep(0.5)


def start_consuming():
    print(" [*] In attesa di messaggi dal middleware. Premere CTRL+C per uscire.")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    # Idempotenza: assicuriamo l'esistenza della coda
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # QoS: evita che un worker riceva più di 1 messaggio alla volta
    channel.basic_qos(prefetch_count=1)

    # Sottoscrizione alla coda
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=process_data
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        start_consuming()
    except KeyboardInterrupt:
        print("Interruzione manuale del servizio consumer.")
