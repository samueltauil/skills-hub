"""Stage timing for the collection pipeline.

Stages run concurrently, so the stage total exceeds the elapsed wall clock.
"""

import contextlib
import threading
import time
from typing import Any, Dict, Iterator, List


class StageTimer:
  """Records wall-clock durations for named pipeline stages. Thread safe."""

  def __init__(self) -> None:
    self._lock = threading.Lock()
    self._stages: List[Dict[str, Any]] = []
    self._t0 = time.monotonic()

  @contextlib.contextmanager
  def stage(self, name: str) -> Iterator[None]:
    """Times the enclosed block, recording it even when it raises."""
    start = time.monotonic()
    try:
      yield
    finally:
      end = time.monotonic()
      with self._lock:
        self._stages.append({
            "stage": name,
            "seconds": round(end - start, 2),
            "started_at": round(start - self._t0, 2),
        })

  def profile(self) -> Dict[str, Any]:
    """Returns the recorded stages, slowest first, plus elapsed wall clock."""
    with self._lock:
      stages = sorted(self._stages, key=lambda s: s["seconds"], reverse=True)
    return {
        "elapsed_seconds": round(time.monotonic() - self._t0, 2),
        "stages": stages,
    }

  def render(self) -> str:
    """Formats the profile as a table for stdout."""
    profile = self.profile()
    lines = [
        f"[COLLECTION PROFILE] elapsed {profile['elapsed_seconds']:.1f}s",
        f"  {'stage':<42} {'seconds':>8}  {'start':>7}",
    ]
    for entry in profile["stages"]:
      lines.append(
          f"  {entry['stage']:<42} {entry['seconds']:>8.2f}"
          f"  {entry['started_at']:>7.2f}"
      )
    return "\n".join(lines)
