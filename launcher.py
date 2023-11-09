import psutil  # Used to check if game profile is running
import time  # Used to delay between launching accounts
import subprocess  # Used to launch hydra launcher and detach from game clients from parent process

HYDRA_LAUNCHER_PATH = "../hydra-launcher-1.0.3.jar"  # Launcher path
ACCOUNTS_PATH = "./accounts.txt"  # Account text file path
LAUNCH_DELAY = 15  # Delay between launching accounts

# Parse account row into email, runelite profile, hydra profile, and proxy
def parse_account(account):
    email = account.split("|")[0]
    runelite_profile = account.split("|")[1]
    hydra_profile = account.split("|")[2]
    proxy = account.split("|")[3]
    return email, runelite_profile, hydra_profile, proxy


# Check if game profile is running by checking if the profile is in the command line arguments of the java process
def is_game_profile_process_running(profile):
    for process in psutil.process_iter(attrs=["pid", "cmdline"]):
        try:
            cmd_line = process.info["cmdline"]
            if cmd_line and f"-profile={profile}" in cmd_line and "java" in cmd_line[0]:
                # print(cmd_line)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# Launch game profile with hydra launcher
def launch_game(account):
    # Parse account
    email, runelite_profile, hydra_profile, proxy = parse_account(account)
    if is_game_profile_process_running(email):
        print(f"Account {email} is already running. Skipping...")
        return
    print(
        f"Launching {email} on proxy {proxy} with profile {runelite_profile} and hydra profile {hydra_profile}"
    )
    try:
        return subprocess.Popen(
            [
                "java",
                "-jar",
                HYDRA_LAUNCHER_PATH,  # Hydra launcher path
                f"-profile={runelite_profile}",  # Runelite profile
                f"-hydraprofile={hydra_profile}",  # Hydra profile
                f"-proxy={proxy}",  # Proxy
                "--scale=1",
            ],  # Client scale. 1.0 default. Lower = smaller. Higher = bigger
            stdout=subprocess.DEVNULL,  # Redirect stdout to nullto prevent spam
        )
    except Exception as e:
        print(f"Failed to launch {email}: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return launch_game(account)


# Read accounts from file in the format of email|runelite_profile|hydra_profile|proxy:port:username:password
def read_accounts_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


# Monitor processes and relaunch crashed processes
def monitor_processes():
    accounts = read_accounts_from_file(ACCOUNTS_PATH)
    print(f"Loading {len(accounts)} accounts...")
    processes = [None] * len(accounts)

    for i, account in enumerate(accounts):
        processes[i] = launch_game(account)
        time.sleep(LAUNCH_DELAY)

    while True:
        for i, account in enumerate(accounts):
            email, runelite_profile, hydra_profile, proxy = parse_account(account)
            if not is_game_profile_process_running(runelite_profile):
                print(f"{email} crashed! Relaunching...")
                processes[i] = launch_game(account)
                time.sleep(LAUNCH_DELAY)

        time.sleep(1)


monitor_processes()
