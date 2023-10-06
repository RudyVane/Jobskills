final: _prev: let
  inherit (final) callPackage;
in {
  jobskills = callPackage ({
    poetry2nix,
    python3,
  }:
    poetry2nix.mkPoetryApplication {
      projectDir = with final.lib.fileset;
        toSource {
          root = ./.;
          fileset = unions [
            ./src
            ./tests
            ./pyproject.toml
            ./poetry.lock
            ./README.md
          ];
        };
      python = python3;
      overrides = poetry2nix.overrides.withDefaults (_self: super: {
        flask = super.flask.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.flit-core];
        });
        aiofiles = super.aiofiles.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.hatchling];
        });
        quart = super.quart.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.poetry];
        });
        twisted = super.twisted.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.hatch-fancy-pypi-readme];
        });
        dynaconf = super.dynaconf.overridePythonAttrs (old: {
          nativeBuildInputs = (old.nativeBuildInputs or []) ++ [super.setuptools];
        });
      });

      pythonImportsCheck = [
        "jobskills.flask"
        "jobskills.discord.jobs.worker"
        "jobskills.scraper.worker"
        # doesn't import without env...
        # "jobskills.gpt.gpt"
      ];

      checkPhase = ''
        runHook preCheck
        pytest
        runHook postCheck
      '';
    }) {};

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
        "jobskills.scraper.worker.WorkerSettings"
        "-v"
      ];
      "discord-worker" = [
        "arq"
        "jobskills.discord.jobs.worker.WorkerSettings"
        "-v"
      ];
    };
  };

  docker-image = callPackage ({
    # self,
    lib,
    dockerTools,
    docker-commands,
  }:
    dockerTools.streamLayeredImage {
      name = "jobskills";
      contents = [
        dockerTools.usrBinEnv
      ];
      config = {
        Env = [
          "PATH=${lib.makeBinPath [docker-commands]}"
        ];
        Entrypoint = ["/usr/bin/env"];
      };

      # created = "@${toString self.sourceInfo.lastModified}";
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
