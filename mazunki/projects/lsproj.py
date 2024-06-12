#!/usr/bin/env python
import os
import json
import argparse
import sys
import pathlib

from .types import PortageSystemRepo, UnixRepo, GitRepo, Repo

repotypes = (GitRepo,)


def test_and_set_project(dir: pathlib.Path) -> None | Repo:
    for repotype in repotypes:
        if repotype.is_repo(dir):
            return repotype(dir)


def find_projects_over(directory: pathlib.Path, root_directory) -> list[Repo]:
    projects = []
    dir = pathlib.Path(directory).resolve()
    while dir != root_directory:
        if repo := test_and_set_project(pathlib.Path(dir)):
            projects.append(repo)
        dir = dir.parent
    return projects


def find_projects_under(directory: pathlib.Path) -> list[Repo]:
    projects = []
    for dirpath, _, _ in os.walk(directory):
        if repo := test_and_set_project(pathlib.Path(dirpath)):
            projects.append(repo)

    return projects


def list_projects(dir, args):
    root_path = pathlib.Path("/" if args.system else os.getenv("HOME", "~"))
    cwd = pathlib.Path(dir)

    # over_paths = find_projects_over(cwd, root_path)
    under_paths = find_projects_under(cwd)

    projects = under_paths

    if args.json:
        print(json.dumps([proj.__json__() for proj in projects], indent=4))
    else:
        for proj in projects:
            print(proj)

    return projects


def main(*args):
    parser = argparse.ArgumentParser(description="List projects on the system")
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output in JSON format"
    )
    parser.add_argument(
        "--system", action="store_true", help="Include system directories"
    )
    parser.add_argument("dirs", nargs="*", help="directory to start from")
    args = parser.parse_args()
    dirs = args.dirs if args.dirs else [os.curdir]

    for dir in dirs:
        list_projects(dir, args)


if __name__ == "__main__":
    main(sys.argv)
