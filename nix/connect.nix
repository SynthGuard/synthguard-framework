{ nixpkgs ? fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11"
, pkgs ? import nixpkgs { }
, fetchurl ? pkgs.fetchurl
}:
pkgs.mkShell
rec {

  buildInputs = [
    pkgs.minikube
  ];

  # Shell Hook Scripts

  ## Shell Hook Entry Script 
  shellHookEntryScript = pkgs.writeShellScript "shellHookEntryScript.sh" ''
    alias kubectl='minikube kubectl --'
    
    # until kubectl get pod -n portainer -o jsonpath='{.items[0].status.phase}' 2>/dev/null | grep -q "Running"; do sleep 1; echo "Waiting for Portainer to start..."; done

    echo "Portainer is running and can be accessed via:"
    minikube service -n portainer --all --url --https
    echo "To delete the minikube cluster run the following command:"
    echo "minikube delete"    
  '';

  ## Shell Hook Exit Script 
  shellHookExitScript = pkgs.writeShellScript "shellHookExitScript.sh" ''
    echo "Exiting..."
    echo "If you accidentally exited this shell, connect again:"
    echo "nix-shell connect.nix"
    echo ""
    echo "To delete the minikube cluster, run:"
    echo "nix-shell connect.nix"
    echo "minikube delete"
  '';

  # Shell Hooks
  shellHook = ''
    source ${shellHookEntryScript}
    trap ${shellHookExitScript} EXIT
  '';
}
