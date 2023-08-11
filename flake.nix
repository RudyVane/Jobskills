{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      p2nix = poetry2nix.legacyPackages.${system};
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      packages = {
        myapp = p2nix.mkPoetryApplication {
          projectDir = self;
          python = pkgs.python311;
        };
        docker-image = let
          env = self.packages.${system}.myapp.dependencyEnv;
        in
          pkgs.dockerTools.streamLayeredImage {
            name = "jobskills";
            config.Cmd = [
              "${env}/bin/gunicorn"
              "-k"
              "uvicorn.workers.UvicornWorker"
              "-b"
              "[::]:8080"
              "jobskills.flask:app"
            ];

            created = "@${toString self.sourceInfo.lastModified}";
          };

        deploy-image = let 
          stream = self.packages.${system}.docker-image;
        in pkgs.writeShellApplication {
          name = "deploy-docker-image";
          runtimeInputs = [ pkgs.skopeo ];
          text = ''
            ${stream} | \
              skopeo copy --dest-precompute-digests \
              docker-archive:/dev/stdin "$(echo "$1" | tr '[:upper:]' '[:lower:]'):${stream.imageTag}"
          '';
        };

        inherit (pkgs) skopeo;
      };

      devShells.default = pkgs.mkShell {
        packages = [pkgs.poetry pkgs.skopeo pkgs.python311 pkgs.alejandra];
      };
    });
}
