#!/usr/bin/env python
# pkg(mazunki)/pythoning/xdg/__init__.py
import os

home = os.path.expanduser("~")

xdg_data_home = os.getenv("XDG_DATA_HOME") or (
    XDG_DATA_HOME := os.path.join(home, ".local", "share")
)
xdg_state_home = os.getenv("XDG_STATE_HOME") or (
    XDG_STATE_HOME := os.path.join(home, ".local", "state")
)
xdg_config_home = os.getenv("XDG_CONFIG_HOME") or (
    XDG_CONFIG_HOME := os.path.join(home, ".config")
)
xdg_cache_home = os.getenv("XDG_CACHE_HOME") or (
    XDG_CACHE_HOME := os.path.join(home, ".cache")
)
xdg_runtime_dir = os.getenv("XDG_RUNTIME_DIR") or (
    XDG_RUNTIME_DIR := os.path.join("/tmp", "user", str(os.getuid()))
)

xdg_data_dirs = os.getenv(
    "XDG_DATA_DIRS", default="/usr/local/share/:/usr/share/"
).split(":")
xdg_config_dirs = os.getenv("XDG_CONFIG_DIRS", default="/etc/xdg").split(":")


def data_path(app: str) -> str:
    return os.path.join(xdg_data_home, app)


def state_path(app: str) -> str:
    return os.path.join(xdg_state_home, app)


def config_path(app: str) -> str:
    return os.path.join(xdg_config_home, app)


def cache_path(app: str) -> str:
    return os.path.join(xdg_cache_home, app)


def runtime_path(app: str) -> str:
    return os.path.join(xdg_runtime_dir, app)
