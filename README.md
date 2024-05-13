# Microservice Application

This repository contains a microservice application designed to demonstrate basic operational functionality, including endpoints for health checks, readiness checks, and metrics collection. The application is developed using Python, containerized with Docker, and deployable via Kubernetes.

## Overview

The service includes the following endpoints:

- `/health`: Returns a 200 OK status if the service is healthy.
- `/ready`: Indicates whether the service is ready to process requests.
- `/payload`: Generates a Fibonacci sequence and returns it in a JSON response.
- `/metrics`: Provides basic operational metrics of the service.

## Prerequisites

To run this application, you will need:

- Docker
- Kubernetes (Minikube or any other Kubernetes cluster setup)


## Project Structure
```bash
.
├── Dockerfile
├── README.md
├── api.py
├── app-manifests.yaml
├── app.py
├── perf-app
│   ├── Dockerfile
│   ├── perf.py
│   └── requirements.txt
├── requirements.txt
└── unittests.py
```

## Setup Instructions

### Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/nezakoo/basic-microservice-application.git
cd basic-microservice-application
```

### Build the Docker Image

Navigate to the directory containing the Dockerfile and build the Docker image:

```bash
docker build -t microservice-app:latest .
```

### Deploy to Kubernetes

Assuming you have a Kubernetes cluster configured (like Minikube), apply the Kubernetes manifests:

> Note: for Minikube use: `eval $(minikube docker-env)` to make images available to Minikube

```bash
kubectl apply -f app-manifests.yaml
```

This command deploys the microservice and creates the necessary Kubernetes objects, such as Deployment and Service.

### Verify the Deployment

Check the status of your deployment:

```bash
kubectl get deployments
kubectl get pods
```

Ensure that the pods are running without issues:

```bash
kubectl logs -f [pod-name]
```

### Accessing the Service

If you are using Minikube, you can access the service using:

```bash
minikube service basic-app-service
```

For other Kubernetes environments, ensure you have the right access configurations or use port-forwarding:

```bash
kubectl port-forward service/basic-app-service 5000:5000
```

Now, you can access the service at `http://localhost:5000`.

## Testing the Service

Run the provided unit tests to ensure everything is functioning correctly:

```bash
python -m unittest discover
```
## Performance Testing

Build the performance testing Docker image:

```bash
cd perf-app
docker build -t perf-app:latest .
```

Run the performance testing container:

```bash
docker run -it --rm --network host -e PYTHONUNBUFFERED=1 perf-app http://host.docker.internal:5030

docker run -it --rm -e PYTHONUNBUFFERED=1 perf-app:latest <service-url> <num-requests> <num-concurrent-requests>
```
> Note: for local testing use `--network host` and `http://host.docker.internal:5000` as the service-url

Reports will be generated in the `./output` directory.

## Using the Microservice

To send requests to the microservice and see it in action, use the following commands:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/ready
curl http://localhost:5000/payload
curl http://localhost:5000/metrics
```

Replace `localhost` with the appropriate IP if running in a different environment.

## Additional Notes

- Customize the deployment configurations in `app-manifests.yaml` to suit your environment needs.
- Monitor the application metrics through Prometheus if configured.
