# ML DevSecOps Demo: AI-Powered Intrusion Detection

## Project Overview

This project demonstrates an AI-powered intrusion detection system using a model trained on the CICIDS2017 dataset. It serves as a demonstration for ML DevSecOps practices, incorporating FastAPI for the inference service, Docker for containerization, Kubernetes for orchestration, and a GitLab CI/CD pipeline for automated build, test, and deployment.

The core of the project is a machine learning model that predicts network intrusions based on flow features. The inference service exposes an API endpoint for these predictions.

## Project Structure

A brief overview of the main directories and files:

*   `inference_service/`: Contains the FastAPI application, Dockerfile for the service, the ML model (`model.joblib`), feature configuration (`feature_config.json`), and related Python scripts.
*   `k8s/`: Holds Kubernetes deployment and service manifests (`fastapi-deployment.yaml`, `fastapi-service.yaml`).
*   `terraform/`: Includes Terraform scripts for infrastructure provisioning (details not covered in this README section).
*   `scripts/`: Contains helper and utility scripts for local testing and model inspection.
*   `.gitlab-ci.yml`: Defines the GitLab CI/CD pipeline for automated build, test, packaging, and deployment.
*   `docker-compose.yml`: Facilitates local development and testing of the inference service and associated services like Prometheus and Grafana.
*   `prometheus.yml`: Configuration file for Prometheus.

## Local Setup and Running

To build and run the service locally:

1.  **Ensure Docker and Docker Compose are installed.**
2.  **Navigate to the project root directory.**
3.  **Run Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image for the inference service and start all defined services.

4.  **Available Services:**
    *   **Inference Service (app):** `http://localhost:8000`
    *   **Prometheus:** `http://localhost:9090`
    *   **Grafana:** `http://localhost:3000`

5.  **Testing the Inference Service:**
    Once the services are running, you can send a test request using `test_client.py`:
    ```bash
    python inference_service/test_client.py
    ```
    This script sends a sample request to the `/predict` endpoint.

## Configuration

*   **Model Path:** The inference service (`inference_service/app.py`) loads the machine learning model from a path specified by the `MODEL_FILE_PATH` environment variable.
    *   In `docker-compose.yml`, this is set to `/app/model.joblib` (pointing to the model file mounted into the container).
    *   If the environment variable is not set, `app.py` defaults to loading `model.joblib` from its current working directory.
*   **Feature Configuration:** The list of feature names used by the model is loaded from `inference_service/feature_config.json`. This file ensures that the input data for predictions is correctly structured.

## CI/CD Pipeline (`.gitlab-ci.yml`)

The project includes a GitLab CI/CD pipeline defined in `.gitlab-ci.yml` with the following stages:

1.  **`build`**: Builds the Docker image for the inference service.
2.  **`test`**: Runs tests against the built Docker image (e.g., using `test_client.py` after starting the service).
3.  **`package`**: Saves the Docker image as a `.tar` artifact.
4.  **`push_to_registry`**: Loads the image artifact, tags it with the commit SHA, and pushes it to a configured container registry.
5.  **`deploy_to_k8s`**: Deploys the application to a Kubernetes cluster using the image pushed in the previous stage. It updates the image tag in `k8s/fastapi-deployment.yaml`.

**GitLab CI/CD Variables:**

To use the CI/CD pipeline, especially the `push_to_registry` and `deploy_to_k8s` stages, you need to configure the following CI/CD variables in your GitLab project settings (Settings > CI/CD > Variables):

*   `CI_REGISTRY`: The URL of your container registry (e.g., `registry.gitlab.com`, `your.private.registry.com`). GitLab's built-in registry usually uses `registry.gitlab.com`.
*   `CI_REGISTRY_USER`: The username for authenticating with the container registry. For GitLab's registry, this is often `gitlab-ci-token`.
*   `CI_REGISTRY_PASSWORD`: The password or access token for the container registry. For GitLab's registry, this is the `$CI_JOB_TOKEN`.
*   `CI_REGISTRY_IMAGE`: The full name of the image in the registry (e.g., `yourgitlabgroup/yourprojectname/cicids-inference` or `yourdockerhubusername/yourimagename`). This should point to where the image will be stored.
*   `KUBE_CONFIG_DATA`: The base64 encoded content of your Kubernetes configuration file (`kubeconfig`). This allows the CI/CD pipeline to authenticate and interact with your Kubernetes cluster. You can get this by running `cat ~/.kube/config | base64 -w0`.

Images built by the pipeline are tagged with the short commit SHA (`$CI_COMMIT_SHORT_SHA`), ensuring unique and traceable image versions.

## Scripts (`scripts/` directory)

The `scripts/` directory contains helper scripts:

*   `train_local.py`: Sends a dummy POST request with random features to the locally running inference service's `/predict` endpoint. Useful for quick end-to-end testing of the service.
*   `check_features.py`: Loads the `model.joblib` file and prints the number of features the model expects. Useful for verifying model compatibility.

## Cleanup Note

There are several unreviewed Python scripts in the `inference_service/` directory:
*   `checking.py`
*   `checking2.py`
*   `inspect_model.py`
*   `extract_columns.py`

These scripts appear to be experimental or for one-off tasks. They should be reviewed: document their purpose, move them to the `scripts/` directory if they are useful utilities, or remove them if they are obsolete to maintain project clarity and reduce clutter.
