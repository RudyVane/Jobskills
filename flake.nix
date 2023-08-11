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
  }: flake-utils.lib.simpleFlake {
    inherit self nixpkgs;
    name = "outputs";
    overlay = ./overlay.nix;
    preOverlays = [
      (_: _: { inherit self; })
      (final: prev: let 
        result = poetry2nix.overlay final prev;
      in builtins.removeAttrs result [ "poetry" ])
    ];
  };
}
