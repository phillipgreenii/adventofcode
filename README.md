# Overview

My solutions to https://adventofcode.com/

# Status

<!-- STATUS_TABLE_START -->
| Year           | Stars |
|:---------------|------:|
| [2023](./2023) |    32 |
| [2022](./2022) |    39 |
| [2021](./2021) |     0 |
| [2020](./2020) |     0 |
| [2019](./2019) |     0 |
| [2018](./2018) |     0 |
| [2017](./2017) |     0 |
| [2016](./2016) |     0 |
| [2015](./2015) |    11 |
<!-- STATUS_TABLE_END -->

# Configuration

## git-crypt

* Install [git-crypt](https://github.com/AGWA/git-crypt)
* Ensure `git-crypt` key is located at `~/.secrets/aoc-git-crypt.key` with permissions of 600
* Run `git-crypt unlock ~/.secrets/aoc-git-crypt.key` on fresh systems


## nix

The solutions in here rely on [nix](https://nix.dev/install-nix.html).  Make sure it is installed.

Second, the following should be in `$HOME/.config/nix/nix.conf`

```
experimental-features = nix-command flakes
bash-prompt-prefix = NIX|
```
