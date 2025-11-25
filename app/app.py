from flask import Flask, request, jsonify
import time
import logging
from pythonjsonlogger import jsonlogger

# Prometheus
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os

# OpenTelemetry (Jaeger)
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# logging: JSON formatter for Loki
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s')
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request latency', ['endpoint'])

app = Flask(__name__)

# setup tracing
resource = Resource.create(attributes={"service.name": "obs-demo-app"})
provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("OTEL_EXPORTER_JAEGER_AGENT_HOST", "jaeger"),
    agent_port=int(os.getenv("OTEL_EXPORTER_JAEGER_AGENT_PORT", 6831)),
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/metrics")
def metrics():
    # expose prometheus default metrics
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route("/")
def hello():
    start = time.time()
    with tracer.start_as_current_span("hello-handler"):
        # simulate work
        time.sleep(0.05)
        resp = {"message": "hello world"}
        status = 200
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/", status=str(status)).inc()
    logger.info("handled root", extra={"request_id": request.headers.get("X-Request-ID", "none"), "path": "/"})
    return jsonify(resp), status

@app.route("/work")
def work():
    start = time.time()
    with tracer.start_as_current_span("work-handler"):
        # simulate variable work
        delay = float(request.args.get("t", "0.1"))
        time.sleep(min(delay, 2.0))
        status = 200
        resp = {"worked": True, "delay": delay}
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/work").observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint="/work", status=str(status)).inc()
    logger.info("handled work", extra={"request_id": request.headers.get("X-Request-ID", "none"), "path": "/work", "delay": delay})
    return jsonify(resp), status

# health
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
