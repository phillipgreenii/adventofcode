{
  description = "Advent Of Code 2023 clojure development environment";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let 
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };
         in
        {
          devShell = import ./shell.nix { inherit pkgs; };
        }
      );
}