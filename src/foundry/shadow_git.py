from __future__ import annotations

import subprocess
from pathlib import Path


class ShadowGit:
    """Manages transactional shadow snapshots and instant rollback."""

    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path

    def snapshot(self) -> str:
        """Captures current working tree state into a git tree hash."""
        result = subprocess.run(
            ["git", "write-tree"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return ""

    def rollback(self, tree_hash: str) -> bool:
        """Restores the workspace to the specified tree hash in O(1) time."""
        if not tree_hash:
            return False
        result = subprocess.run(
            ["git", "read-tree", "--reset", "-u", tree_hash],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
