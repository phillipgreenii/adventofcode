{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
    overriden-vscode = pkgs.vscode-with-extensions.override {
      vscodeExtensions = with pkgs.vscode-extensions; [
        golang.go
      ];
    };
in
mkShell {
  nativeBuildInputs = [
    go
    gopls
    overriden-vscode
  ];
}