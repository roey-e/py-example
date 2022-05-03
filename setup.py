from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py
from distutils.command.clean import clean as _clean

import itertools
import os
import re


def parse_c_enum(lines):
    enum_name = None
    entries = {}

    for line in lines:
        try:
            enum_name, *_ = re.findall(r"enum (\w+)", line)
        except ValueError:
            pass
        entries.update(re.findall(r"(\w+)\s*=\s*(\d+)", line))

    return enum_name, entries

def generate_python_enum(enum_name, entries):
    return "\n".join(
        itertools.chain(
            ["import enum", f"class {enum_name}(enum.Enum):"],
            (f"    {key} = {value}" for key, value in entries.items())
        )
    ) + "\n"


class MyPythonSourceGenerator(_build_py):
    def run(self):
        with open("example/header.h", "r") as header_file:
            lines = header_file.readlines()
        enum_name, entries = parse_c_enum(lines)
        code = generate_python_enum(enum_name, entries)
        with open("example/generated.py", "w") as python_file:
            python_file.write(code)

        _build_py.run(self)

class MyClean(_clean):
    def run(self):
        if os.path.exists("example/generated.py"):
            os.remove("example/generated.py")

        _clean.run(self)

def build(setup_kwargs):
    setup_kwargs.update({
        "cmdclass": {
            "clean": MyClean,
            "build_py": MyPythonSourceGenerator,
        }
    })

setup_kwargs = {
    "name": "example",
    "packages": find_packages(),
}
build(setup_kwargs)
setup(**setup_kwargs)