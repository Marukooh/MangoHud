"""Check that user-facing overlay options appear in both reference files."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INTERNAL_OPTIONS = {
    "blacklist",
    "fsr_steam_sharpness",
    "inherit",  # Preset configuration directive, not a MangoHud.conf option.
    "mangoapp_steam",
    "media_player_format",
    "pci_dev",
    "read_cfg",  # Only meaningful in MANGOHUD_CONFIG.
}


def main():
    header = (ROOT / "src/overlay_params.h").read_text()
    readme = (ROOT / "README.md").read_text()
    config = (ROOT / "data/MangoHud.conf").read_text()

    options = set(re.findall(
        r"^\s*OVERLAY_PARAM_(?:BOOL|CUSTOM)\((\w+)\)", header, re.MULTILINE
    )) - INTERNAL_OPTIONS
    missing = []

    for option in sorted(options):
        if not re.search(rf"`{re.escape(option)}(?:\s*=[^`]*)?`", readme):
            missing.append(f"README.md: {option}")
        if not re.search(rf"^\s*(?:#\s*)?{re.escape(option)}(?:\s*=.*)?\s*$", config, re.MULTILINE):
            missing.append(f"data/MangoHud.conf: {option}")

    if missing:
        raise SystemExit("Undocumented options:\n" + "\n".join(missing))

    print(f"Checked {len(options)} overlay options")


if __name__ == "__main__":
    main()
