{
  description = "Deep Rock Galactic Deep Dive Tracker";

  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-unstable";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
    inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
      pkgs = import nixpkgs {inherit system;};
    in {
      formatter = pkgs.alejandra;
      packages = rec {
        deep-dive-tracker = mkPoetryApplication { projectDir = self; python = pkgs.python311; };
        default = deep-dive-tracker;
        docker = pkgs.dockerTools.buildLayeredImage {
          name = "deep-dive-tracker";
          tag = "latest";
          contents = [ default ];
          extraCommands = ''
          mkdir -p app
          '';
          config.Cmd = [ "${default}/bin/drg-dd-tracker" ];
          config.WorkingDir = "/app";
        };
      };
      devShells.default = pkgs.mkShell {
        packages = [poetry2nix.packages.${system}.poetry ];
      };
    });
}
