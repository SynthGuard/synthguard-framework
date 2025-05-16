{ nixpkgs ? fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11"
, pkgs ? import nixpkgs { }
, fetchurl ? pkgs.fetchurl
}:
pkgs.mkShell 
rec {
  buildInputs = [
    pkgs.minikube
    pkgs.docker
  ];

  portainerVersion = "ce2-19";

  portainerNodePort = fetchurl {
    url = "https://downloads.portainer.io/${portainerVersion}/portainer.yaml";
    hash = "sha256-11wXW6a/II07n7BhxBfBXtoTgziLqq/N+e3Qiaq7lEk=";
  };

  # Build the Docker image
  dockerBuildScript = pkgs.writeShellScript "dockerBuildScript.sh" ''
    # echo "Building Docker image..."
  '';

  # Shell Hook Entry Script
  shellHookEntryScript = pkgs.writeShellScript "shellHookEntryScript.sh" ''
    echo "Adjusting inotify settings..."

    # Build the Docker image
    
    echo "Starting Minikube..."
    alias kubectl='minikube kubectl --'
    # minikube start
    minikube start --memory=8096 --cpus=8 --disk-size=30g

    echo "Installing Portainer ${portainerVersion}"
    kubectl apply -n portainer -f ${portainerNodePort}
    until kubectl get pod -n portainer -o jsonpath='{.items[0].status.phase}' 2>/dev/null | grep -q "Running"; do
      sleep 1
      echo "Waiting for Portainer to start..."
    done

    echo "Portainer is running and can be accessed via:"
    minikube service -n portainer --all --url --https

    # export PIPELINE_VERSION=2.3.0
    # kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
    # kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
    # kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
    
    export PIPELINE_VERSION=2.0.0
    kubectl apply --kustomize="github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION&timeout=90s"
    kubectl wait crd/applications.app.k8s.io --for=condition=established --timeout=60s
    kubectl apply --kustomize="github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION&timeout=90s"

    echo "Waiting for Kubeflow components to settle..."

    while true; do
      total_pods=$(kubectl get pods -A --no-headers | wc -l)
      running_pods=$(( $(kubectl get pods -A --field-selector=status.phase==Running --no-headers | wc -l) + $(kubectl get pods -A --field-selector=status.phase==Succeeded --no-headers | wc -l) ))
      non_running_pods=$(kubectl get pods -A --field-selector=status.phase!=Running --no-headers)
      echo "Pods running: $running_pods/$total_pods"
      if [ "$non_running_pods" ]; then
        echo "Non-running pods:"
        echo "$non_running_pods"
      fi

      # Check if 'admission-webhook-deployment' pod is in CrashLoopBackOff
      if kubectl get pods -A --field-selector=status.phase!=Running | grep 'admission-webhook-deployment' | grep 'CrashLoopBackOff'; then
        echo "Pod 'admission-webhook-deployment' is in CrashLoopBackOff. Adjusting inotify settings..."
        sudo sysctl fs.inotify.max_user_instances=1280
        sudo sysctl fs.inotify.max_user_watches=655360
      fi

      if [ "$running_pods" -eq "$total_pods" ]; then
        break
      fi
      sleep 30
    done
    
    echo "Creating secret for Docker credentials..."
    kubectl create secret docker-registry regcred -n kubeflow \
    --docker-server=<DOCKER_SERVER> \
    --docker-username=<DOCKER_USERNAME> \
    --docker-password=<DOCKER_PASSWORD> \
    --docker-email=<DOCKER_EMAIL>


    echo "Setting up port forwarding for Kubeflow dashboard..."
    kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80 &
    
    echo 'Setting up port forwarding for MINIO dashboard'
    kubectl get secret mlpipeline-minio-artifact -n kubeflow -o jsonpath="{.data.accesskey}" | base64 --decode
    kubectl get secret mlpipeline-minio-artifact -n kubeflow -o jsonpath="{.data.secretkey}" | base64 --decode
    kubectl port-forward -n kubeflow svc/minio-service 9000:9000

    echo "To delete the minikube cluster run the following command:"
    echo "minikube delete"
  '';

  # Shell Hook Exit Script
  shellHookExitScript = pkgs.writeShellScript "shellHookExitScript.sh" ''
    echo "Exiting..."
    echo "If you accidentally exited this shell, connect again:"
    echo "nix-shell connect.nix"
    echo ""
    echo "To delete the minikube cluster, run:"
    echo "nix-shell connect.nix && minikube delete"
  '';

  # Shell Hooks
  shellHook = ''
    source ${shellHookEntryScript}
    trap "source ${shellHookExitScript}" EXIT
  '';
}