# iqstars

Python app for playing [IQ Stars](https://www.smartgames.eu/uk/one-player-games/iq-stars).

## Requirements

The following dependencies must already be installed on your system:

| Dependency                                  | Version |
| ------------------------------------------- | ------- |
| [python](https://www.python.org/downloads/) | ^3.12   |
| [pipx](https://pipx.pypa.io/stable/)        | ^1.6    |

## Setup

Install the app using `pipx`, e.g. directly from GitHub using SSH:

```
$ pipx install git+ssh://git@github.com/own-neufeldm/iqstars.git

  installed package iqstars 1.0.0, installed using Python 3.12.5
  These apps are now globally available
    - iqstars.exe
done! ✨ 🌟 ✨
```

You can now run the app using `iqstars`.

## Usage

Modify the board and pieces ([here](./iqstars/main.py)) for which the app should find solutions for.
Then, run `iqstars`.
