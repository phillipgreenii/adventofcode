{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
    python = pkgs.python3Minimal;
    overriden-vscode = pkgs.vscode-with-extensions.override {
      vscodeExtensions = with pkgs.vscode-extensions; [
              ms-python.isort
              ms-python.python
              ms-python.vscode-pylance
      ];
    };
in
mkShell {
  nativeBuildInputs = [
    (python.withPackages (ps: with ps; [

    ]))
    overriden-vscode
  ];
}