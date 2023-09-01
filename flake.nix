{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
  inputs.poetry2nix = {
    url = "github:K900/poetry2nix/new-bootstrap-fixes";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.treefmt-nix = {
    url = "github:numtide/treefmt-nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    systems,
    poetry2nix,
    treefmt-nix,
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
        })
        (final: prev: let
          result = poetry2nix.overlay final prev;
        in
          builtins.removeAttrs result ["poetry"])
      ];
    }
    // eachSystem (system: {
      formatter = self.legacyPackages.${system}.treefmtEval.config.build.wrapper;
    });
}
