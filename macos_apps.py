import psutil
from typing import Optional
from AppKit import NSWorkspace
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
)
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    kAXFocusedWindowAttribute,
    kAXTitleAttribute,
)
import plistlib
from pathlib import Path


workspace = NSWorkspace.sharedWorkspace()

def get_app_name_from_bundle(running_app) -> str:
    try:
        bundle_url = running_app.bundleURL()
        if not bundle_url:
            return running_app.localizedName()

        bundle_path = Path(bundle_url.path())
        app_folder_name = bundle_path.stem
        if app_folder_name:
            return app_folder_name

        info_plist = bundle_path / "Contents" / "Info.plist"
        if info_plist.exists():
            with info_plist.open("rb") as f:
                plist = plistlib.load(f)
                return (
                    plist.get("CFBundleDisplayName")
                    or plist.get("CFBundleName")
                )

        return running_app.localizedName()
    except Exception:
        return running_app.localizedName()

def get_open_pids() -> set:
    return {
        app.processIdentifier()
        for app in workspace.runningApplications()
        if app.processIdentifier() is not None
    }


def get_window_title_ax(pid: int) -> Optional[str]:
    try:
        app_ref = AXUIElementCreateApplication(pid)

        result, window = AXUIElementCopyAttributeValue(
            app_ref, kAXFocusedWindowAttribute, None
        )
        if result != 0 or window is None:
            return None

        result, title = AXUIElementCopyAttributeValue(
            window, kAXTitleAttribute, None
        )
        if result != 0:
            return None

        return title
    except Exception:
        return None


def get_active_app() -> dict:
    app = workspace.activeApplication()
    pid = app["NSApplicationProcessIdentifier"]

    process = psutil.Process(pid)
    process_name = process.name().lower()

    running_app = next(
        (a for a in workspace.runningApplications()
         if a.processIdentifier() == pid),
        None
    )

    if running_app:
        app_name = get_app_name_from_bundle(running_app)
    else:
        app_name = app["NSApplicationName"]

    window_title = get_window_title_ax(pid)

    if not window_title:
        windows = CGWindowListCopyWindowInfo(
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )
        for w in windows:
            if w.get("kCGWindowOwnerPID") == pid and w.get("kCGWindowLayer") == 0:
                window_title = w.get("kCGWindowName", "")
                if window_title:
                    break

    if not window_title:
        window_title = app_name

    return {
        "pid": pid,
        "process_name": process_name,
        "app_name": app_name,
        "window_title": window_title,
    }
