import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "numpy",
        "gymnasium",
        "pygame",
        "matplotlib",
        "pandas",
        "environment",
        "agents",
        "training",
        "evaluation",
        "experiments",
    ],
)
def test_required_module_import(module_name):
    module = importlib.import_module(module_name)
    assert module is not None