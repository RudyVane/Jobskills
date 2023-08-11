final: prev: let
  inherit (final) callPackage;
in {
  jobskills = callPackage ({
    self,
    poetry2nix,
    python311,
  }:
    poetry2nix.mkPoetryApplication {
      projectDir = self;
      python = python311;
    }) {};

  docker-entrypoints = callPackage ({
    lib,
    jobskills,
    writeShellApplication,
    symlinkJoin,
    # input
    commands,
  }: let
    mkCommand = name: cmd:
      writeShellApplication {
        inherit name;
        runtimeInputs = [jobskills.dependencyEnv];
        text = ''
          ${lib.escapeShellArgs cmd} "$@"
        '';
      };
  in
    symlinkJoin {
      name = "docker-commands";
      paths = lib.mapAttrsToList mkCommand commands;
    }) {
    commands = {
      "discord-endpoint" = [
        "gunicorn"
        "-k"
        "uvicorn.workers.UvicornWorker"
        "jobskills.flask:asgi_app"
      ];
      "scrape-worker" = [
        "arq"
        "jobskills.scrape.WorkerConfig"
      ];
    };
  };

  docker-image = callPackage ({
    self,
    lib,
    dockerTools,
    dash,
    docker-entrypoints,
  }:
    dockerTools.streamLayeredImage {
      name = "jobskills";
      config = {
        Env = [
          "PATH=${lib.makeBinPath [docker-entrypoints]}"
        ];
        Entrypoint = [
          (lib.getExe dash)
          "-c"
        ];
      };

      created = "@${toString self.sourceInfo.lastModified}";
    }) {};

  deploy-image = callPackage ({
    skopeo,
    writeShellApplication,
    docker-image,
  }:
    writeShellApplication {
      name = "deploy-docker-image";
      runtimeInputs = [skopeo];
      text = ''
        repo=$(echo "$1" | tr '[:upper:]' '[:lower:]')
        tag="${docker-image.imageTag}"
        ${docker-image} | \
          skopeo copy --dest-precompute-digests \
          docker-archive:/dev/stdin "$repo:$tag"
        skopeo copy "$repo:$tag" "$repo:latest"
      '';
    }) {};

  outputs = {
    inherit
      (final)
      jobskills
      docker-entrypoints
      docker-image
      deploy-image
      skopeo
      ;

    checks = {
      # add derivations here to run during check
      inherit (final) jobskills;
    };
  };
}
