import time
from macos_apps import get_active_app, get_open_pids
from model import AppTracker
from discord_rpc import DiscordRPC
from config_loader import load_final_config

# Simple timestamped logger for key events
log = lambda msg: print(f"[{time.strftime('%H:%M:%S')}] {msg}")

DISCORD_CLIENT_ID, WHITELIST = load_final_config()

tracker = AppTracker(WHITELIST)
rpc = DiscordRPC(DISCORD_CLIENT_ID)
last_app = None

rpc_active = False
recon = False

while True:
    try:
        if recon:
            log("Reconnecting to Discord RPC...")
            rpc.reconnect()
            log("Reconnected to Discord RPC")
            recon = False

        active = get_active_app()
        open_pids = get_open_pids()

        tracker.update_open_apps(open_pids)
        tracker.add_or_update(active)

        process_name = active["process_name"]

        if process_name in tracker.whitelist:
            tracker.set_focus(active["pid"])
            app = tracker.apps.get(active["pid"])
            if app != last_app:
                last_app = app
                log(f"Now tracking: {app.app_name} ({app.process_name})")
            if app:
                if not rpc.connected:
                    log("RPC not connected; attempting reconnection...")
                    rpc.reconnect()
                    log("RPC connection restored")

                payload = rpc.update(app)
                # print("RPC payload:", payload)

        else:
            tracker.last_focused_pid = None
    except Exception as e:
        log(f"RPC error: {e}; will retry in 5s")
        recon = True
        time.sleep(5)

    time.sleep(1)
