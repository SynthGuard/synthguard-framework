# SynthGuard Framework User Manual

## List of Contents

1. Workflow Execution Deployment (Nix + Minikube + KFP)
2. Running Pipelines
3. Setting up Docker Image
4. Developing SDG Pipelines with the Automation Tool

## Workflow Execution Deployment (Nix + Minikube + KFP)

### For linux:
Run the `linux-script.sh` script located in the `nix/` directory:
```bash ./nix/linux-script.sh```

### For Windows/MacOS:
1. Install Nix.
2. Run the following command to start the Kubeflow Pipelines (KFP) environment:
```nix-shell nix/kfp-start.nix```

Access on localhost:8080

Connect to the cluster by running:
```nix-shell nix/connect.nix```

## Running Pipelines

### Steps to Run a Pipeline

1. Navigate to the `pipelines/` directory, which contains subfolders for each demo pipeline (e.g., `TEADAL`, `iris_pipeline`, `LAGO`).
2. Choose the desired pipeline YAML file (e.g., `LAGO_pipeline.yaml`).
3. Open the KFP dashboard at `localhost:8080`.
4. Go to the **Pipelines** tab and click **Upload Pipeline**.
5. Choose the YAML file and provide a name if prompted.

### After Upload

1. Click **Create Run**.
2. Set pipeline parameters (if applicable).
3. Click **Start** to execute.

### Monitoring

- Follow execution status in the graphical DAG.
- Click on individual components to view logs, outputs, and visualizations.
- Download output artifacts or open generated HTML reports.

## Setting up Docker image

1. Build the Docker image using the Dockerfile located in the docker/ directory:
```docker build -t <your-docker-registry>/<image-name>:<tag> docker/```
2. Push the image to your chosen Docker registry:
```docker push <your-docker-registry>/<image-name>:<tag>```
3. Add the registry credentials to nix/kfp-start.nix before running it
4. Define base image using kfp SDK

## Develop SDG pipeline with automation tool

1. Create a configuration file for your pipeline and save it in the automation/configs/ directory.
2. Specify file location in automation/main.py
3. Run main.py
4. Open the generated notebook from the automation/generated_content/ directory and run the methods locally to validate them.
5. Adjust the notebook for Kubeflow Pipelines (KFP) compatibility if needed.
