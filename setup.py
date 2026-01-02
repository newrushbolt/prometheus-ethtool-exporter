#!/usr/bin/env python
"""Setup.py for setuptools and debian packaging."""
from setuptools import find_packages, setup
from subprocess import CalledProcessError, DEVNULL, check_output
import re


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


def closest_tag():
    """Find the closest/latest tag in the repository."""
    try:
        tag = (
            check_output(["git", "describe", "--tags"], stderr=DEVNULL)
            .decode("utf-8")
            .lstrip("v")
            .split("-")[0]  # Get the tag part, ignore commit count and hash
            .strip()
        )
    except (CalledProcessError, FileNotFoundError):
        tag = ""
    return tag


def version():
    tag = git_tag()
    
    if tag:
        base_version = tag
    else:
        # Try to find the closest tag if we're not on an exact tag
        closest = closest_tag()
        if closest:
            base_version = closest
        else:
            # No tags found, use branch name
            base_version = git_branch()
    
    sha = git_commit()

    # Sanitize base_version to be PEP 440 compliant
    # Replace hyphens and underscores with dots
    base_version = re.sub(r"[-_]", ".", base_version)
    
    # PEP 440 requires version to start with a digit
    # If it doesn't, use a default version and include branch/tag info in local identifier
    if not re.match(r"^\d", base_version):
        # Use default dev version and include sanitized branch/tag name in local identifier
        version_str = f"0.0.0.dev0+{base_version}.{sha}"
    else:
        # Build version string with local version identifier (PEP 440 compliant)
        version_str = f"{base_version}+{sha}"

    return version_str


setup(
    name="ethtool_exporter",
    version=version(),
    description="ethtool exporter",
    scripts=["ethtool_exporter.py"],
    py_modules=[],
)
