# 📄 Progetto Universitario (PW): Middleware Sicuro per Industria 4.0

### **Titolo Completo:**
Implementazione di un Middleware Asincrono e Sicuro per la Gestione della Telemetria nel Settore Manifatturiero.

---

## 🎯 **Obiettivo del Progetto**

Questo progetto implementa una soluzione di **Middleware orientata allo scambio di messaggi asincroni** per affrontare i requisiti di affidabilità, scalabilità e sicurezza nella comunicazione tra i dispositivi IIoT (Industrial Internet of Things) e i sistemi di supervisione (SCADA/Backend) in un contesto industriale.

Il sistema è progettato per **disaccoppiare** i produttori di dati (Sensori/Macchinari) dai consumatori (Servizi di analisi e allarme), garantendo la **persistenza dei messaggi** (resilienza) e predisponendo meccanismi di **sicurezza** (autenticazione, crittografia end-to-end).

---

## 🛠️ **Architettura e Tecnologie Adottate**

| Componente | Ruolo | Tecnologia/Linguaggio |
| :--- | :--- | :--- |
| **Broker/Middleware** | Gestisce le code, disaccoppia i servizi, garantisce l'affidabilità. | **RabbitMQ** (Implementato con Docker) |
| **Producer** | Simula un Sensore Industriale che invia dati (telemetria e allarmi). | Python 3 + `pika` (client AMQP) |
| **Consumer** | Simula il Backend/Sistema SCADA che riceve, elabora e logga i dati. | Python 3 + `pika` (client AMQP) |
| **Infrastruttura** | Permette l'orchestrazione rapida e replicabile dei servizi. | **Docker** e **Docker Compose** |

### Diagramma Architetturale
Per una visione d'insieme della struttura del progetto, fare riferimento al **Diagramma Architetturale** incluso nell'elaborato [Figure 1].

---

## 🚀 **Setup e Avvio del Progetto**

Il progetto è containerizzato per facilità di esecuzione. Sono necessari **Docker** e **Docker Compose** installati sul sistema host.

### 1. Avvio del Middleware e dell'Infrastruttura
Aprire il terminale nella directory principale del progetto e lanciare il file `docker-compose.yml`:

```bash
docker-compose up -d
