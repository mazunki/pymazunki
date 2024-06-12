#!/usr/bin/env python

import importlib
import sys, os


def main(subproject, *subproject_args, invoke="main"):
    subprojects = {
        "chronos": "mazunki.chronos.__main__",
        "fs": "mazunki.fs.__main__",
        "projects": "mazunki.projects.lsproj",
        "minecraft": "mazunki.minecraft.__main__",
        "pythoning": "mazunki.pythoning.__main__",
        "format": "mazunki.pythoning.fmt.formatters",
    }
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if subproject not in subprojects:
        print(f"Unknown subproject: {subproject}")
        sys.exit(1)

    subproject_module = subprojects[subproject]
    module = importlib.import_module(subproject_module)

    if hasattr(module, invoke):
        sys.argv[0] = sys.argv[0] + ":" + sys.argv.pop(1)
        module.__dict__[invoke](*subproject_args)
    else:
        print(f"No main() function defined in {subproject_module}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m mazunki [test] <subproject> [args...]")
        sys.exit(1)

    if sys.argv[1] == "test":
        main(sys.argv[2], invoke="test", *sys.argv[3:])
    else:
        main(sys.argv[1], invoke="main", *sys.argv[2:])


#  vim: set sts=4 sw=4 ts=4 expandtab
