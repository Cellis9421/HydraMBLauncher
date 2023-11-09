# Hydra Multibox Manager

## About

This script will launch multiple game clients using the hydra launcher. It will also monitor the game clients and relaunch any crashed clients.
This script is useful for running multiple accounts on a single computer (multiboxing).
It is recommended to use a seperate RL, Hydra, and proxy for each account.

## Prerequisites:

1. Java 8 or higher (installed as PATH variable)
2. Runelite (https://runelite.net/)
3. Hydra launcher (Discord)
4. Accounts.txt file with accounts in the format of email|runelite_profile|hydra_profile|proxy:port:username:password

## Accounts.txt example:

One row per account

```
email|runelite_profile|hydra_profile|proxy:port:username:password
email|runelite_profile|hydra_profile|proxy:port:username:password
email|runelite_profile|hydra_profile|proxy:port:username:password
```

## How It Works

We start by loading all account from the provided path in the config.
We then launch one client for each account with the provided profiles, account, and proxy.
When launching each game client, an account specific parameter is passed to the process.
We then check that each account is still running by looking for a living process with the respective account specific parameter.
If none is found, we relaunch that game client with the profile, account, and proxy from the accounts.txt file.

## Configs

```
HYDRA_LAUNCHER_PATH = "../hydra-launcher-1.0.3.jar"  # Launcher path
ACCOUNTS_PATH = "./accounts.txt"  # Account text file path
LAUNCH_DELAY = 15  # Delay between launching accounts
```

## How To Start

Run the script

Aboslute pathing
```
python C:\path\to\your\launcher.py
```

Relative pathing
```
python .\launcher.py
```
