final: _prev: let
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
      overrides = poetry2nix.overrides.withDefaults (_self: super: {
        flask = super.flask.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.flit-core];
        });
      });
    }) {};

  docker-entrypoint = callPackage ({writeShellScriptBin}:
    writeShellScriptBin "docker-entrypoint" ''
      exec $@
    '') {};

  docker-commands = callPackage ({
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
          exec ${lib.escapeShellArgs cmd} "$@"
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
        "jobskills.scraper.worker.WorkerConfig"
      ];
    };
  };

  docker-image = callPackage ({
    self,
    lib,
    dockerTools,
    docker-commands,
    docker-entrypoint,
  }:
    dockerTools.streamLayeredImage {
      name = "jobskills";
      config = {
        Env = [
          "PATH=${lib.makeBinPath [docker-commands]}"
        ];
        Entrypoint = [(lib.getExe docker-entrypoint)];
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
      docker-commands
      docker-image
      deploy-image
      skopeo
      treefmtEval
      ;

    checks = {
      # add derivations here to run during check
      inherit (final) jobskills pre-commit-check;
      formatting = final.treefmtEval.config.build.check final.self;
    };
  };
}
