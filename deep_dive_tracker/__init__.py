import time

import schedule

from deep_dive_tracker.api import get_current_deep_dives
from deep_dive_tracker.config import load_config, save_config
from deep_dive_tracker.deep_dive import DeepDiveSet
from deep_dive_tracker.discord import send_discord_message

configuration = load_config()


def should_send(current: DeepDiveSet):
    global configuration
    state = configuration.get("state", {})

    for variant in current.variants:
        saved_seed = state.get(variant.get_type(), None)
        if saved_seed is None or saved_seed != variant.seed:
            return True
    return False


def update_state(current: DeepDiveSet):
    global configuration
    state = configuration.get("state", {})
    for variant in current.variants:
        state[variant.get_type()] = variant.seed

    configuration["state"] = state
    save_config(configuration)


def poll_and_send():
    current = get_current_deep_dives()
    if current is None:
        print("Failed to get current deep dives")
    if should_send(current):
        print("New Deep Dives")
        send_discord_message(configuration.get("webhook"), current)
        update_state(current)
    else:
        print("No new deep dives")


def main():
    global configuration
    if configuration.get("webhook") is None:
        print("No webhook configured")
        exit(1)
    schedule.every().hour.at("00:00").do(poll_and_send)

    print("Initialized!")

    poll_and_send()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
