# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Load the scripts as modules: they live in directories, not in a package."""

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent


def load(name: str, path: str) -> ModuleType:
    """Import the script at path, relative to the repository, under name."""
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        msg = f"cannot load {path}"
        raise ImportError(msg)
    module = importlib.util.module_from_spec(spec)
    # dataclasses look their module up while the script runs.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def theme() -> ModuleType:
    """theme/source/generate.py."""
    return load("theme_generate", "theme/source/generate.py")


@pytest.fixture(scope="session")
def logo() -> ModuleType:
    """logo/source/generate.py."""
    return load("logo_generate", "logo/source/generate.py")


@pytest.fixture(scope="session")
def package() -> ModuleType:
    """logo/source/package.py."""
    return load("logo_package", "logo/source/package.py")


@pytest.fixture(scope="session")
def ascii_logo() -> ModuleType:
    """logo/ascii/ascii-logo.py."""
    return load("ascii_logo", "logo/ascii/ascii-logo.py")
