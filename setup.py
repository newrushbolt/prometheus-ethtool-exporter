#!/usr/bin/env python
"""Setup.py for setuptools and debian packaging."""
from setuptools import find_packages, setup
from subprocess import CalledProcessError, check_output


def version():
    try:
        version = (
            check_output(["git", "describe", "--exact-match", "--tags"])
            .decode("utf-8")
            .lstrip("v")
            .strip()
        )
    except (CalledProcessError, FileNotFoundError):
        version = "unknown"
    try:
        sha = check_output(["git", "rev-parse", "HEAD"]).decode("utf-8")[:8]
    except (CalledProcessError, FileNotFoundError):
        sha = "unknown"
    return f"{version}+{sha}"


setup(
    name="ethtool_exporter",
    version=version(),
    description="ethtool exporter",
    scripts=["ethtool_exporter.py"],
    py_modules=[],
)
