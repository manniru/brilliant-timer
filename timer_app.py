#!/usr/bin/env python3
import rumps
import time
from datetime import datetime, timedelta

class BrilliantTimer(rumps.App):
    def __init__(self):
        super(BrilliantTimer, self).__init__("⏱")
        
        # Initialize variables
        self.stopwatch_active = False
        self.timer_active = False
        self.start_time = 0
        self.elapsed_time = 0
        self.timer_end_time = None
        
        # Configure menu items
        self.stopwatch_button = rumps.MenuItem("Start Stopwatch")
        self.timer_button = rumps.MenuItem("Start Timer (5m)")
        self.reset_button = rumps.MenuItem("Reset")
        self.timer_10m = rumps.MenuItem("Start Timer (10m)")
        self.timer_15m = rumps.MenuItem("Start Timer (15m)")
        self.timer_30m = rumps.MenuItem("Start Timer (30m)")
        
        # Add menu items
        self.menu = [
            self.stopwatch_button,
            None,  # Separator
            self.timer_button,
            self.timer_10m,
            self.timer_15m,
            self.timer_30m,
            None,  # Separator
            self.reset_button
        ]
        
        # Start update timer
        self.timer = rumps.Timer(self.update_timer, 0.1)
        self.timer.start()

    @rumps.clicked("Start Stopwatch")
    def toggle_stopwatch(self, _):
        if not self.timer_active:
            if not self.stopwatch_active:
                self.start_time = time.time() - self.elapsed_time
                self.stopwatch_active = True
                self.stopwatch_button.title = "Stop Stopwatch"
            else:
                self.stopwatch_active = False
                self.elapsed_time = time.time() - self.start_time
                self.stopwatch_button.title = "Start Stopwatch"

    def start_countdown(self, minutes):
        if not self.stopwatch_active:
            self.timer_active = True
            self.timer_end_time = datetime.now() + timedelta(minutes=minutes)
            self.timer_button.title = f"Stop Timer ({minutes}m)"
            self.title = f"⏱ {minutes}:00"

    @rumps.clicked("Start Timer (5m)")
    def toggle_timer(self, _):
        if not self.timer_active:
            self.start_countdown(5)
        else:
            self.timer_active = False
            self.timer_button.title = "Start Timer (5m)"
            self.title = "⏱"

    @rumps.clicked("Start Timer (10m)")
    def start_timer_10m(self, _):
        self.start_countdown(10)

    @rumps.clicked("Start Timer (15m)")
    def start_timer_15m(self, _):
        self.start_countdown(15)

    @rumps.clicked("Start Timer (30m)")
    def start_timer_30m(self, _):
        self.start_countdown(30)

    @rumps.clicked("Reset")
    def reset(self, _):
        self.stopwatch_active = False
        self.timer_active = False
        self.elapsed_time = 0
        self.timer_end_time = None
        self.stopwatch_button.title = "Start Stopwatch"
        self.timer_button.title = "Start Timer (5m)"
        self.title = "⏱"

    def update_timer(self, _):
        if self.stopwatch_active:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            self.title = f"⏱ {minutes}:{seconds:02d}"
        
        elif self.timer_active:
            remaining = self.timer_end_time - datetime.now()
            if remaining.total_seconds() <= 0:
                self.timer_active = False
                self.timer_button.title = "Start Timer (5m)"
                self.title = "⏱"
                rumps.notification(
                    title="Timer Complete",
                    subtitle="Your timer has finished!",
                    message=""
                )
            else:
                minutes = int(remaining.total_seconds() // 60)
                seconds = int(remaining.total_seconds() % 60)
                self.title = f"⏱ {minutes}:{seconds:02d}"

if __name__ == "__main__":
    BrilliantTimer().run() 