"""Simple task scheduler."""

import threading
import time
from typing import Callable, Optional
from .core import TaskManager, TaskStatus


class Scheduler:
    """A simple scheduler for running tasks."""

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Start the scheduler."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run(self):
        """Main scheduler loop."""
        while self._running:
            pending = self.task_manager.list_tasks(status=TaskStatus.PENDING)
            for task in pending:
                self.task_manager.update_task_status(task.id, TaskStatus.RUNNING)
            time.sleep(5)

    def schedule_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        **kwargs,
    ) -> bool:
        """
        Schedule a function to run as a task.

        Args:
            task_id: The task ID to update.
            func: The function to call.
            *args, **kwargs: Arguments to pass to the function.

        Returns:
            True if successful.
        """
        task = self.task_manager.get_task(task_id)
        if not task:
            return False

        try:
            result = func(*args, **kwargs)
            self.task_manager.complete_task(task_id, result={"output": str(result)})
            return True
        except Exception as e:
            self.task_manager.update_task_status(
                task_id, TaskStatus.FAILED, error=str(e)
            )
            return False
