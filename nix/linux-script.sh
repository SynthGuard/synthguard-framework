#!/bin/bash

# Function to check if a program is installed
check_program() {
  command -v "$1" >/dev/null 2>&1
}

# Nix script path 
script_path="minikube/kfp-start.nix"

# Check for Nix and Docker
if ! check_program nix; then
  echo "Installing Nix..."
  sudo apt-get update
  sudo apt-get install nix
fi

if ! check_program docker; then
  echo "Installing Docker..."
  sudo apt-get update && sudo apt-get install -y docker.io
  # Start the Docker service
  sudo systemctl start docker

  # Add user to docker group (if needed)
  sudo usermod -aG docker $USER && newgrp docker

  # Log out and back in for changes to take effect
  echo "Please log out and back in for Docker configuration to be complete."
fi

# Run the Nix script
echo "Running Nix script: $script_path"
nix-shell "$script_path" 