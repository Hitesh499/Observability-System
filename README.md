# Observability-System

## 1. Overview

This project demonstrates how to build a complete observability stack using:
| Component             | Purpose                               |
| --------------------- | ------------------------------------- |
| **Prometheus**        | Collects & stores application metrics |
| **Grafana**           | Visualizes metrics, logs, and traces  |
| **Loki**              | Centralized log storage               |
| **Promtail**          | Log collector for Loki                |
| **Jaeger**            | Distributed tracing                   |
| **Flask Application** | Demo service with metrics/tracing     |
| **Docker Compose**    | Orchestrates all services             |

This system helps you monitor:<br/>
Application performance metrics<br/>
Application & system logs<br/>
Complete request trace flow across services<br/>

## 2. Architecture

**Flow:**
```
                       ┌──────────────┐
                       │   Grafana    │
                       │  Dashboards  │
                       └──────┬───────┘
                Metrics       │      Logs & Traces
                              │
     ┌───────────┬────────────┴──────────┬───────────┐
     │           │                        │           │
┌────────┐  ┌──────────┐        ┌─────────────┐   ┌──────────┐
│  App   │→│Prometheus │→────→  │    Loki     │←──│ Promtail │
│        │  │          │        │ (Log Store) │   │ (Logs)   │
└────────┘  └──────────┘        └─────────────┘   └──────────┘
      │
      ↓  Traces
 ┌─────────────┐
 │   Jaeger    │
 └─────────────┘
```

## 3. Project Structure
```
ObservabilitySystem/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── prometheus/
│   └── prometheus.yml
│
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── observability-datasources.yml
│   │   └── dashboards/
│   │       └── observability-dashboard.yml
│   └── dashboards-json/
│       └── observability.json
│
├── loki/
│   └── loki-config.yaml
│
├── promtail/
│   └── promtail-config.yaml
│
└── docker-compose.yml
```

## 4. How to Run the Observability System
Step 1 — Start All Services
```
docker compose up --build
```

Step 2 — Confirm All Containers Are Running<br/>
You should see:<br/>
1. app<br/>
2. prometheus<br/>
3. grafana<br/>
4. loki<br/>
5. promtail<br/>
6. jaeger<br/>

## 5. Access the Tools
| Tool                      | URL                                              |
| ------------------------- | ------------------------------------------------ |
| **Flask App**             | [http://localhost:5000](http://localhost:5000)   |
| **Prometheus Metrics UI** | [http://localhost:9090](http://localhost:9090)   |
| **Grafana Dashboard**     | [http://localhost:3000](http://localhost:3000)   |
| **Jaeger Tracing UI**     | [http://localhost:16686](http://localhost:16686) |


## 6. Validation Checklist

1️⃣ Metrics Check<br/>
Open: http://localhost:5000/metrics<br/>
Prometheus target status: http://localhost:9090/targets<br/>
Targets must show: Up<br/>

2️⃣ Logs Check<br/>
Open Grafana → Explore → Loki<br/>
Run query:<br/>
{job="app_logs"}<br/>
Or:<br/>
{job="varlogs"}<br/>

3️⃣ Traces Check<br/>
Open: http://localhost:16686<br/>
Select service: flask-app<br/>
Click Search Traces → traces must appear.<br/>

4️⃣ Grafana Dashboard Check<br/>
Login:<br/>
Username: admin<br/>
Password: admin<br/>
Dashboards auto-load from:<br/>
grafana/dashboards-json/<br/>

## 7. Configurations Used

1. Prometheus
Scrapes metrics from the Flask app<br/>
Scrapes itself<br/>
File: prometheus/prometheus.yml<br/>

2. Grafana
Auto-provisioned dashboards
Auto-configured Prometheus + Loki data sources
Files:
```
grafana/provisioning/datasources/*.yml
grafana/provisioning/dashboards/*.yml
```

3. Loki
Stores logs locally<br/>
14-day retention<br/>
File: loki/loki-config.yaml<br/>

4. Promtail
Reads logs from:<br/>
/var/log/*.log<br/>
Docker container logs<br/>
File: promtail/promtail-config.yaml <br/>

5. Jaeger
All-in-one tracing setup<br/>
Trace UI at port 16686<br/>

6. Flask App
Includes:<br/>
Prometheus multiprocess metrics<br/>
OpenTelemetry tracing<br/>
Jaeger exporter<br/>
Custom logging<br/>
Environment variables set inside docker-compose.yml.

## 8. To Stop Services
```
docker compose down
```

## 9. Project Completed When…
✔ All containers are healthy
✔ Prometheus shows metrics
✔ Grafana shows dashboards
✔ Loki shows logs
✔ Jaeger shows traces
✔ Flask app responds
✔ No errors in Docker logs

## 10. Conclusion
This project demonstrates a complete end-to-end, offline Observability System integrating:<br/>
1. Metrics<br/>
2. Logs<br/>
3. Traces<br/>
4. Dashboards<br/>
It is ready for learning, demos, and DevOps practice.
