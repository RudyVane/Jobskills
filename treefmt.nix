# treefmt.nix
_: {
  # Used to find the project root
  projectRootFile = "flake.nix";
  programs.alejandra.enable = true;
  programs.black.enable = true;
  programs.isort = {
    enable = true;
    profile = "black";
  };
  programs.taplo.enable = true;
  programs.yamlfmt.enable = true;
}
