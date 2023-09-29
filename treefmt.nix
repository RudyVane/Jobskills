# treefmt.nix
_: {
  # Used to find the project root
  projectRootFile = "flake.nix";
  programs = {
    alejandra.enable = true;
    black.enable = true;
    isort = {
      enable = true;
      profile = "black";
    };
    ruff.enable = true;
    taplo.enable = true;
    yamlfmt.enable = true;
  };
  settings.formatter.yamlfmt.includes = ["*.yaml" "*.yml"];
}
