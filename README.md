# Deep Dive Tracker

A tracker for Deep Rock Galactic Deep Dives, using [DRGApi](https://drgapi.com/)

## Building

Deep Dive Tracker is built with poetry, and requires Python 3.11 due to changes surrounding `datetime.fromisoformat`.

Build using the following command:

```
poetry build
```

### With Nix

Deep Dive Tracker can be built with

```
nix-build
```

or, if using Flakes:

```
nix build
```

## Docker

A docker image can be built with

```
nix-build -A outputs.packages.${system}.docker
```

For example

```
nix-build -A outputs.packages.x86_64-linux.docker
```

or, if using Flakes:

```
nix build .#docker
```

## Configuration

The program looks for a `config.toml` in the current directory, and stores the last seeds of the deep dives in the configuration.

The only key that is requried is `webhook`, which is set to the URL of the Discord webhook that this instance will send to.
