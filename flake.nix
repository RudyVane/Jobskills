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
          overrides = p2nix.overrides.withDefaults (self: super: {
            gunicorn = super.gunicorn.overridePythonAttrs (old: {
              nativeBuildInputs = (old.nativeBuildInputs or []) ++ [self.packaging];
            });

            service-identity = super.service-identity.overridePythonAttrs (old: {
              nativeBuildInputs =
                (old.nativeBuildInputs or [])
                ++ [
                  self.hatchling
                  self.hatch-vcs
                  self.hatch-fancy-pypi-readme
                ];
            });

            flask-discord-interactions = super.flask-discord-interactions.overridePythonAttrs (old: {
              nativeBuildInputs = (old.nativeBuildInputs or []) ++ [self.setuptools];
            });
          });
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

        deploy-image = pkgs.writeShellApplication {
          name = "deploy-docker-image";
          runtimeInputs = [ pkgs.skopeo ];
          text = ''
            ${self.packages.${system}.docker-image} | \
              skopeo copy --dest-precompute-digests \
              docker-archive:/dev/stdin "$@"
          '';
        };

        inherit (pkgs) skopeo;
      };

      devShells.default = pkgs.mkShell {
        packages = [pkgs.poetry pkgs.skopeo pkgs.python311 pkgs.alejandra];
      };
    });
}
