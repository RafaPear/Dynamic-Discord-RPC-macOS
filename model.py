import time
from dataclasses import dataclass
from typing import Optional, Dict, Set


@dataclass
class AppState:
    # Snapshot of a single process plus its focus timing
    app_name: str
    process_name: str
    open_time: float
    window_title: str

    focused_time_total: float = 0.0
    focus_start: Optional[float] = None

    def focus(self) -> None:
        if self.focus_start is None:
            self.focus_start = time.time()

    def unfocus(self) -> None:
        if self.focus_start is not None:
            self.focused_time_total += time.time() - self.focus_start
            self.focus_start = None

    def total_focused_time(self) -> float:
        total = self.focused_time_total
        if self.focus_start is not None:
            total += time.time() - self.focus_start
        return total


class AppTracker:
    def __init__(self, whitelist: Set[str]):
        self.apps: Dict[int, AppState] = {}
        self.whitelist = whitelist
        self.last_focused_pid: Optional[int] = None

    def update_open_apps(self, open_pids: Set[int]) -> None:
        # Drop processes that closed and finalize their focus time
        closed = set(self.apps.keys()) - open_pids
        for pid in closed:
            self.apps[pid].unfocus()
            del self.apps[pid]

    def add_or_update(self, info: dict) -> None:
        pid = info["pid"]
        name = info["app_name"]
        process_name = info["process_name"]

        if process_name not in self.whitelist:
            return

        if pid not in self.apps:
            self.apps[pid] = AppState(
                app_name=name,
                process_name=process_name,
                open_time=time.time(),
                window_title=info["window_title"],
            )
        else:
            self.apps[pid].window_title = info["window_title"]

    def set_focus(self, pid: int) -> None:
        if pid == self.last_focused_pid:
            return

        if self.last_focused_pid in self.apps:
            # Stop timing the previously focused process
            self.apps[self.last_focused_pid].unfocus()

        if pid in self.apps:
            # Start timing the newly focused process
            self.apps[pid].focus()
            self.last_focused_pid = pid
