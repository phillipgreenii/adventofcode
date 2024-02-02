{ pkgs ? import <nixpkgs> {} }:

with pkgs;

let
    jdk = pkgs.jdk17_headless;
    overriden-vscode = pkgs.vscode-with-extensions.override {
      vscodeExtensions = with pkgs.vscode-extensions; [
              betterthantomorrow.calva
      ];
    };
in
mkShell {
  nativeBuildInputs = [
    clojure
    clojure-lsp
    jdk
    leiningen
    overriden-vscode
  ];
}