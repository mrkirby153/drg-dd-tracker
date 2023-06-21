from textwrap import dedent

import requests

import deep_dive_tracker.constants as constants
from deep_dive_tracker.deep_dive import (DeepDive, DeepDiveSet, DeepDiveStage,
                                         DeepDiveType)


def send_discord_message(webhook: str, dive_set: DeepDiveSet) -> bool:
    resp = requests.post(
        webhook,
        json={
            "username": constants.WEBHOOK_NAME,
            "avatar_url": constants.WEBHOOK_AVATAR_URL,
            "content": f"New Deep Dives Available\n\nFrom: <t:{dive_set.start_time.timestamp():.0f}:F>\nTo: <t:{dive_set.end_time.timestamp():.0f}:F>",
            "embeds": [dive_embed(dive) for dive in dive_set.variants],
        },
    )
    return resp.status_code == 204


def _embed_color(stage: DeepDive) -> int:
    if stage.type == DeepDiveType.ELITE:
        return 0xFF0000
    elif stage.type == DeepDiveType.NORMAL:
        return 0xFF6600
    else:
        return 0


def _stage(stage: DeepDiveStage) -> any:
    modifiers = []
    if stage.anomaly:
        modifiers.append(f"Anomaly: {stage.anomaly}")
    if stage.warning:
        modifiers.append(f"Warning: {stage.warning}")
    modifiers = "\n".join(modifiers)
    modifiers_disp = f"\n\n{modifiers}" if modifiers else ""
    return {
        "name": f"Stage {stage.id}",
        "value": f"Primary: {stage.primary}\nSecondary: {stage.secondary}{modifiers_disp}",
        "inline": True,
    }


def dive_embed(dive: DeepDive) -> any:
    return {
        "title": f"{dive.get_type()}: {dive.name}",
        "description": f"Biome: {dive.biome}\nSeed: `{dive.seed}`",
        "fields": [_stage(stage) for stage in dive.stages],
        "color": _embed_color(dive),
    }
