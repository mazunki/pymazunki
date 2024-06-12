#!/usr/bin/env python
# pkg(mazunki)/fs/fs.py
import os
import ctypes
import ctypes.util

import copy
from dataclasses import dataclass
import pathlib


@dataclass
class MountEntry:
    fs_dev: pathlib.Path
    fs_path: pathlib.Path
    fs_type: str
    fs_mountflags: int
    fs_data: list[str]
    fs_dump: int
    fs_pass: int

    mountflags = {
        "lazytime": 1 << 25,  # MS_LAZYTIME
        "mand": 1 << 9,  # MS_MANDLOCK
        "noatime": 1 << 7,  # MS_NOATIME
        "nodev": 1 << 2,  # MS_NODEV
        "nodiratime": 1 << 8,  # MS_NODIRATIME
        "noexec": 1 << 6,  # MS_NOEXEC
        "nosuid": 1 << 5,  # MS_NOSUID
        "relatime": 1 << 21,  # MS_RELATIME
        "sync": 1 << 0,  # MS_SYNCHRONOUS
        "ro": 1 << 1,  # MS_RDONLY
        "remount": 1 << 5,  # MS_REMOUNT
    }

    def __init__(
        self,
        fs_dev: pathlib.Path,
        fs_path: pathlib.Path,
        fs_type: str,
        fs_opts: list[str],
        fs_dump: int,
        fs_pass: int,
    ):
        self.fs_dev = fs_dev
        self.fs_path = fs_path
        self.fs_type = fs_type
        self.fs_dump = fs_dump
        self.fs_pass = fs_pass
        self.fs_mountflags, self.fs_data = self.parse_mountflags(fs_opts)

    @classmethod
    def from_line(cls, line: str):
        parts = line.split()
        return cls(
            fs_dev=pathlib.Path(parts[0]),
            fs_path=pathlib.Path(parts[1]),
            fs_type=parts[2],
            fs_opts=parts[3].split(","),
            fs_dump=int(parts[4]),
            fs_pass=int(parts[5]),
        )

    def parse_mountflags(self, opts: list[str]) -> int:
        data = [
            opt
            for opt in opts
            if opt not in MountEntry.mountflags and opt not in {"rw"}
        ]

        mountflags = 0
        for opt in opts:
            if opt in MountEntry.mountflags:
                mountflags |= MountEntry.mountflags[opt]

        return (mountflags, data)

    def set_readonly(self, state):
        if state == "ro":
            self.fs_mountflags |= MountEntry.mountflags["ro"]
        else:
            self.fs_mountflags &= ~MountEntry.mountflags["ro"]

    def __str__(self):
        newline = "\n"
        return f"""MountEntry(
  fs_dev={self.fs_dev},
  fs_path={self.fs_path},
  fs_type={self.fs_type},
  fs_mountflags={self.fs_mountflags},
  fs_data=[
    {f"{newline}    ".join(self.fs_data)}
  ],
  fs_dump={self.fs_dump},
  fs_pass={self.fs_pass}
)"""


class Filesystem:
    def __init__(self, path: pathlib.Path, *, rw=False):
        self.path: pathlib.Path = pathlib.Path(path)
        self.rw = "rw" if rw else "ro"
        print("Startup:", self.get_mount_info())

        self.original_mount_entry = self.get_mount_info()

    def __enter__(self):
        self.original_mount_entry = self.get_mount_info()

        new_entry = copy.copy(self.original_mount_entry)
        new_entry.set_readonly(self.rw)

        print("Remount:", new_entry, end="\n\n")
        self.remount(new_entry)
        print("Remounted", self.get_mount_info(), end="\n\n")

    def __exit__(self, a, b, c):
        import time

        time.sleep(5)
        print("Leaving", self.get_mount_info(), end="\n\n")

    def get_mount_info(self):
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if pathlib.Path(parts[1]).resolve() == self.path.resolve():
                    return MountEntry.from_line(line)

    def remount(self, mount_entry: MountEntry):
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

        source = ctypes.c_char_p(str(mount_entry.fs_dev).encode("utf-8"))
        target = ctypes.c_char_p(str(mount_entry.fs_path).encode("utf-8"))
        fstype = ctypes.c_char_p(mount_entry.fs_type.encode("utf-8"))
        mountflags = ctypes.c_ulong(mount_entry.fs_mountflags)
        data = ",".join(mount_entry.fs_data).encode("utf-8")
        data_p = ctypes.c_char_p(data)

        print(f"{source=}, {target=}, {fstype=}, {mountflags=}, {data_p=}")
        result = libc.mount(source, target, fstype, mountflags, data_p)
        if result != 0:
            errno = ctypes.get_errno()
            raise OSError(
                errno, f"Failed to remount {mount_entry.fs_path}: {os.strerror(errno)}"
            )
