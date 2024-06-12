#!/usr/bin/env python

import abc
from git import Repo as GitRepository, InvalidGitRepositoryError
from gentoolkit.helpers import FileOwner as PortageFileOwner
from gentoolkit.package import Package as PortagePackage

import pathlib
import typing
import datetime

__all__ = ("GitRepo", "UnixRepo", "PortageSystemRepo", "Repo")
type Repo = GitRepo | PortageSystemRepo | UnixRepo


class UnknownPackageError(RuntimeError):
    def __init__(self, file):
        super().__init__(f"couldn't find the package for owned {file} file")


class ABCRepo(abc.ABC):
    path: pathlib.Path
    name: str
    owner: str
    type_identifier: str

    def __init__(self, path: pathlib.Path | str, name: str, owner: str):
        self.path = path if isinstance(path, pathlib.Path) else pathlib.Path(path)
        self.name = name
        self.owner = owner

    @classmethod
    @abc.abstractmethod
    def is_repo(cls, path: pathlib.Path) -> bool: ...

    @abc.abstractmethod
    def last_modified_date(self) -> datetime.datetime: ...

    def __str__(self):
        return f"{self:%t:%n\t(%o)\t%p\t%e}"

    def __format__(self, fmt):
        specifiers = {
            "n": self.name.removesuffix(".git"),
            "p": str(self.path).replace(str(self.path.home()), ""),
            "t": self.type_identifier,
            "o": self.owner,
            "e": self.last_modified_date(),
        }
        stringbuilder = []

        i = 0
        while i < len(fmt):
            if fmt[i] == "%" and i < len(fmt) - 1:
                i += 1
                if fmt[i] in specifiers:
                    stringbuilder.append(str(specifiers[fmt[i]]))
                    i += 1
                else:
                    raise RuntimeError("Unexpected specifier")
            else:
                stringbuilder.append(fmt[i])
                i += 1

        return "".join(stringbuilder)

    def __json__(self):
        return {
            "name": str(self.name),
            "path": str(self.path),
            "type": str(self.type_identifier),
            "owner": str(self.owner),
            "last_edit": str(self.last_modified_date()),
        }


class GitRepo(ABCRepo):
    type_identifier = "git"

    def __init__(self, path: pathlib.Path):
        self.gitrepo = GitRepository(str(path))
        if self.gitrepo.bare:
            raise NotImplementedError("we don't support bare git repos")

        remotes = self.gitrepo.remotes
        if remotes:
            repoowner, _, reponame = remotes[0].url.partition(":")[2].rpartition("/")
            repoowner = repoowner.split("/")[-1]
        else:
            reponame = path.name
            repoowner = path.owner()

        config = self.gitrepo.config_reader()
        # owner = str(config.get_value("user", "name")) or repoowner
        owner = repoowner

        super().__init__(path, name=reponame, owner=owner)

    @classmethod
    def is_repo(cls, path: pathlib.Path) -> bool:
        try:
            if path.name == ".git":
                return False
            GitRepository(str(path))
            return True
        except InvalidGitRepositoryError:
            return False

    def last_modified_date(self) -> datetime.datetime:
        return self.gitrepo.head.commit.committed_datetime


class PortageSystemRepo(ABCRepo):
    type_identifier = "portage"

    def __init__(self, *files: pathlib.Path):
        self.pkg_owners: list[tuple[PortagePackage, str]] = PortageFileOwner()(
            map(str, files)
        )
        pkg, file = typing.cast(tuple[PortagePackage, str], self.pkg_owners[0])
        self.assumed_package: PortagePackage = pkg
        path = pathlib.Path(file)
        pkgname = str(self.assumed_package)
        super().__init__(path, name=pkgname, owner=pkgname)

    @classmethod
    def is_repo(cls, path: pathlib.Path) -> bool:
        return bool(cls(path))

    def __bool__(self):
        return bool(self.pkg_owners)

    def last_modified_date(self) -> datetime.datetime:
        return datetime.datetime.now()


class UnixRepo(ABCRepo):
    type_identifier = "unix"

    def __init__(self, path: pathlib.Path):
        super().__init__(path, name=path.name, owner=str(path.owner()))

    def last_modified_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.path.stat().st_mtime)

    @classmethod
    def is_repo(cls, path: pathlib.Path) -> bool:
        return bool(path)


def main(paths):
    for path in paths:
        pkg = PortageSystemRepo(pathlib.Path(path))


if __name__ == "__main__":
    main("/etc/nginx")


# vim: set sw=4 ts=4 expandtab
