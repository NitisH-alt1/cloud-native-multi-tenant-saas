\# Kubernetes Deployment



This directory contains the Kubernetes deployment manifests for the

Cloud-Native Multi-Tenant SaaS Platform.



\## Architecture



The Kubernetes deployment contains:



\- `Namespace` for platform isolation

\- PostgreSQL 16 database

\- PersistentVolumeClaim for PostgreSQL storage

\- PostgreSQL Secret

\- PostgreSQL ClusterIP Service

\- FastAPI backend Deployment

\- Backend ConfigMap

\- Backend Secret

\- Backend ClusterIP Service

\- Readiness and liveness probes

\- CPU and memory resource requests/limits



\## Kubernetes Resources



```text

saas-platform namespace

│

├── PostgreSQL

│   ├── Secret

│   ├── PersistentVolumeClaim

│   ├── Deployment

│   └── Service

│

└── Backend

&#x20;   ├── ConfigMap

&#x20;   ├── Secret

&#x20;   ├── Deployment

&#x20;   └── Service

