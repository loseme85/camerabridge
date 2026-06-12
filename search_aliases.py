"""
search_aliases.py
=================
Search-layer alias tables.

These aliases interpret user search terms only. Do not import this module
from classifier stages such as detect_mount, detect_category, auto_label,
or detect_model.
"""

from __future__ import annotations


DEFAULT_BRAND = "Leica"


MODEL_FAMILY_ALIASES: dict[str, str] = {
    "lux": "Summilux",
    "summilux": "Summilux",
    "summilux-m": "Summilux",
    "cron": "Summicron",
    "summicron": "Summicron",
    "summicron-m": "Summicron",
    "summicron-sl": "Summicron",
    "nocti": "Noctilux",
    "noct": "Noctilux",
    "noctilux": "Noctilux",
    "noctilux-m": "Noctilux",
    "elmarit": "Elmarit",
    "elmarit-m": "Elmarit",
    "elmar": "Elmar",
    "summaron": "Summaron",
    "summarit": "Summarit",
    "apo-summicron-sl": "APO-Summicron-SL",
    "apo-summicron-m": "APO-Summicron-M",
    "tri-elmar": "Tri-Elmar",
    "trielmar": "Tri-Elmar",
    "vario-elmarit-sl": "Vario-Elmarit-SL",
    "vario-elmar-r": "Vario-Elmar-R",
    "vario-elmarit-r": "Vario-Elmarit-R",
    "mp3": "MP3",
    "cm": "CM",
}


MODEL_SYSTEM_ALIASES: dict[str, str] = {
    "cm": "PNS",
}


VARIANT_ALIASES: dict[str, str] = {
    "aa": "AA",
    "asph": "ASPH",
    "aspherical": "ASPH",
    "pre-asph": "pre-ASPH",
    "preasph": "pre-ASPH",
    "fle": "FLE",
    "fle2": "FLE2",
    "close-focus": "FLE2",
    "rigid": "Rigid",
    "dr": "Dual Range",
    "dualrange": "Dual Range",
    "dual-range": "Dual Range",
    "8매": "8-element",
    "8-element": "8-element",
    "8element": "8-element",
    "silver": "Silver",
    "black-paint": "Black Paint",
    "blackpaint": "Black Paint",
}


GENERATION_ALIASES: dict[str, str] = {
    "1st": "1st",
    "first": "1st",
    "v1": "1st",
    "1세대": "1st",
    "2nd": "2nd",
    "second": "2nd",
    "v2": "2nd",
    "2세대": "2nd",
    "3rd": "3rd",
    "third": "3rd",
    "v3": "3rd",
    "3세대": "3rd",
    "4th": "4th",
    "fourth": "4th",
    "v4": "4th",
    "4세대": "4th",
}


MOUNT_ALIASES: dict[str, str] = {
    "m": "M",
    "m-mount": "M",
    "m_mount": "M",
    "m마운트": "M",
    "ltm": "L",
    "l39": "L",
    "m39": "L",
    "screw": "L",
    "sl": "SL",
    "l-mount": "SL",
    "l_mount": "SL",
    "l마운트": "SL",
    "r": "R",
    "s": "S",
}


SYSTEM_ALIASES: dict[str, str] = {
    "q": "Q",
    "q2": "Q",
    "q3": "Q",
    "d-lux": "Compact",
    "dlux": "Compact",
    "minilux": "PNS",
    "sofort": "Compact",
}
