# treefmt.nix
{...}: {
  # Used to find the project root
  projectRootFile = "flake.nix";
  programs.alejandra.enable = true;
  programs.deadnix.enable = true;
  #FIXME: enable and fix errors
  #programs.ruff.enable = true;
  programs.black.enable = true;
}
