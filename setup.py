#!/usr/bin/env python
"""Setup.py for setuptools and debian packaging."""
from setuptools import find_packages, setup
from subprocess import CalledProcessError, DEVNULL, check_output


def git_branch():
    try:
        branch = (
            check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode("utf-8")[:8]
            .strip()
        )
    except (CalledProcessError, FileNotFoundError):
        branch = "unknown"
    return branch


def git_commit():
    try:
        sha = check_output(["git", "rev-parse", "HEAD"]).decode("utf-8")[:8].strip()
    except (CalledProcessError, FileNotFoundError):
        sha = "unknown"
    return sha


def git_tag():
    try:
        tag = (
            check_output(["git", "describe", "--exact-match", "--tags"], stderr=DEVNULL)
            .decode("utf-8")
            .lstrip("v")
            .strip()
        )
    except (CalledProcessError, FileNotFoundError):
        tag = ""
    return tag


def version():
    tag = git_tag()
    version = tag if tag else git_branch()
    sha = git_commit()
    return f"{version}+{sha}"


setup(
    name="ethtool_exporter",
    version=version(),
    description="ethtool exporter",
    scripts=["ethtool_exporter.py"],
    py_modules=[],
)
