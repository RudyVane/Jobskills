{
  description = "Application packaged using poetry2nix";

  inputs = {
    systems.url = "github:nix-systems/x86_64-linux";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    poetry2nix = {
      #url = "github:nix-community/poetry2nix";
      url = "github:gekoke/poetry2nix/9c970f4c554c870286c0ba84b9bb3f6ba56d0a9d"; # PR 1541
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
        systems.follows = "systems";
      };
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
      };
    };
    nix-github-actions = {
      url = "github:nix-community/nix-github-actions";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    systems,
    poetry2nix,
    treefmt-nix,
    nix-github-actions,
    pre-commit-hooks,
  }: let
    systems' = import systems;
    eachSystem = flake-utils.lib.eachSystem systems';
  in
    flake-utils.lib.simpleFlake {
      inherit self nixpkgs;
      systems = systems';
      name = "outputs";
      overlay = ./overlay.nix;
      preOverlays = [
        (_: _: {inherit self;})
        (pkgs: _: {
          treefmtEval = treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
          pre-commit-check = pre-commit-hooks.lib.${pkgs.system}.run {
            src = self;
            hooks = {
              # Python
              #FIXME mypy.enable = true;
              ruff.enable = true;

              # Nix
              deadnix.enable = true;
              statix.enable = true;

              # yaml
              actionlint.enable = true;
              #FIXME yamllint.enable = true;
            };
          };
        })
        poetry2nix.overlays.default
      ];
    }
    // eachSystem (system: {
      formatter = self.legacyPackages.${system}.treefmtEval.config.build.wrapper;
    })
    // {
      githubActions = nix-github-actions.lib.mkGithubMatrix {inherit (self) checks;};
    };
}
