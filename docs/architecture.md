# Synthguard Framework

The Synthguard Framework is a modular and extensible system designed to facilitate the generation, processing, and evaluation of synthetic data pipelines. It is structured to support a variety of use cases, including data preprocessing, synthetic data generation, privacy and utility evaluation, and integration with Kubeflow Pipelines for scalable workflows.

### 1. **`automation/`**
Automates the generation of pipeline notebooks and configurations.
- `main.py`: Entry point for generating pipeline notebooks.
- `notebook_generator.py`: Contains logic for creating Jupyter notebooks based on pipeline configurations.
- `configs/`: Stores JSON configuration files for pipelines.
- `generated_content/`: Contains auto-generated pipeline notebooks.

### 2. **`docker/`**
- `Dockerfile`: Defines the base image and dependencies for running the framework in a containerized environment.

### 3. **`docs/`**
- `architecture.md`: Describes the architecture of the framework.
- `usage.md`: Provides instructions for using the framework.

### 4. **`nix/`**
Contains Nix scripts for setting up the development environment and deploying pipelines.
- `connect.nix`: Configures connections for external services.
- `kfp-start.nix`: Automates the setup of Kubeflow Pipelines and related services.

### 5. **`pipelines/`**
Houses pipeline definitions and related components. Each subdirectory represents a specific pipeline with YAML definitions, notebooks, and scripts.

### 6. **`synthguard-library/`**
Core library containing reusable modules for data processing, synthetic data generation, and evaluation.
-  `synthguard/`: Contains Python modules for helper functions, data preprocessing, synthetic data generation, and report generation.