# Example

This Poetry example installs the package using `build.py` in an editable manner, **not** generating `generated.py` in-project.

`poetry build` calls `build.py` which generates the python source file `generated.py`:
```
roey@penguin:~/py-example$ poetry build
The virtual environment found in /home/roey/py-example/.venv seems to be broken.
Recreating virtualenv example in /home/roey/py-example/.venv
Building example (0.1.0)
  - Building sdist
  - Built example-0.1.0.tar.gz
  - Building wheel
running build
running build_py
creating /home/roey/py-example/build
creating /home/roey/py-example/build/lib
creating /home/roey/py-example/build/lib/example
copying example/__init__.py -> /home/roey/py-example/build/lib/example
copying example/generated.py -> /home/roey/py-example/build/lib/example
copying example/header.h -> /home/roey/py-example/build/lib/example
  - Built example-0.1.0-cp37-cp37m-manylinux_2_28_aarch64.whl
roey@penguin:~/py-example$ ll dist/example-0.1.0
example-0.1.0-cp37-cp37m-manylinux_2_28_aarch64.whl
example-0.1.0.tar.gz
```

**But** the final wheel doesn't include `generated.py`. In fact it includes `header.h` which is unwanted.
