import argparse
import importlib.util
import sys
from pathlib import Path


def load_config_from_file(path: str):
    path = Path(path)

    if not path.exists():
        print(f"[ERROR] Config file not found: {path}")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("user_config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "DISCORD_CLIENT_ID"):
        print("[ERROR] Config file must define DISCORD_CLIENT_ID")
        sys.exit(1)

    if not hasattr(module, "WHITELIST"):
        print("[ERROR] Config file must define WHITELIST")
        sys.exit(1)

    return module.DISCORD_CLIENT_ID, set(module.WHITELIST)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Dynamic Discord Rich Presence for macOS"
    )

    parser.add_argument(
        "--config",
        default="config.py",
        help="Path to config file (default: config.py)"
    )

    parser.add_argument(
        "--app-id",
        help="Discord Application ID (overrides config file)"
    )

    parser.add_argument(
        "--apps",
        nargs="+",
        help="List of process names to track (overrides config file)"
    )

    return parser.parse_args()


def load_final_config():
    args = parse_args()

    # 1. Load from config file
    app_id, whitelist = load_config_from_file(args.config)

    # 2. Override via CLI
    if args.app_id:
        app_id = args.app_id

    if args.apps:
        whitelist = set(a.lower() for a in args.apps)

    return app_id, whitelist

