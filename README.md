# Example

## Installing
This PDM example installs the package in an editable manner, **not** generating `generated.py` in-project.
```
roey@penguin:~/py-example$ pdm install -v
All packages are synced to date, nothing to do.

Installing the project as an editable package...
Preparing isolated env for PEP 517 build...
Building wheel for file:///home/roey/py-example#egg=example
Collecting setuptools<61,>=42 (from -r /tmp/pdm-build-reqs-lqr02v68.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/7c/5b/3d92b9f0f7ca1645cba48c080b54fe7d8b1033a4e5720091d1631c4266db/setuptools-60.10.0-py3-none-any.whl
Installing collected packages: setuptools
Successfully installed setuptools-60.10.0
Collecting setuptools_pep660 (from -r /tmp/pdm-build-reqs-randdf9t.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/e0/39/00ac158c6ddc1887fe958e5e76c6ce313f16de1966959ccaf2d801778405/setuptools_pep660-0.1.3-py3-none-any.whl
Collecting setuptools<61,>=42 (from setuptools_pep660->-r /tmp/pdm-build-reqs-randdf9t.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/7c/5b/3d92b9f0f7ca1645cba48c080b54fe7d8b1033a4e5720091d1631c4266db/setuptools-60.10.0-py3-none-any.whl
Collecting wheel (from setuptools_pep660->-r /tmp/pdm-build-reqs-randdf9t.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/27/d6/003e593296a85fd6ed616ed962795b2f87709c3eee2bca4f6d0fe55c6d00/wheel-0.37.1-py2.py3-none-any.whl
Installing collected packages: setuptools, wheel, setuptools-pep660
  The script wheel is installed in '/tmp/pdm-build-env-z2x24tzv-shared/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed setuptools-60.10.0 setuptools-pep660-0.1.3 wheel-0.37.1
running editable_wheel
running dist_info
creating /tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info
writing /tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/PKG-INFO
writing dependency_links to /tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/dependency_links.txt
writing top-level names to /tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/top_level.txt
writing manifest file '/tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/SOURCES.txt'
reading manifest file '/tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/SOURCES.txt'
writing manifest file '/tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.egg-info/SOURCES.txt'
creating '/tmp/pdm-wheel-mx82hz7d/tmph1dnqo59/example.dist-info'
running build_ext
Install example 0.1.0 successful

🎉 All complete!
```

PDM uses `setuptools_pep660` as the fallback build beckend for editable packages.

Looking into `setuptools_pep660`'s code, in `editable_wheel.py:63:65`:
```python
        # Build extensions in-place
        self.reinitialize_command("build_ext", inplace=1)
        self.run_command("build_ext")
```
It calls "build_ext" only, leaving "build_py" uncalled.

## Building
`pdm build` calls `setup.py` which generates the python source file `generated.py`:
```
roey@penguin:~/py-example$ pdm build -v
Building sdist...
Preparing isolated env for PEP 517 build...
Collecting setuptools>=36.6.0 (from -r /tmp/pdm-build-reqs-ajdybum7.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/fb/58/9efbfe68482dab9557c49d433a60fff9efd7ed8835f829eba8297c2c124a/setuptools-62.1.0-py3-none-any.whl
Installing collected packages: setuptools
Successfully installed setuptools-62.1.0
running egg_info
creating example.egg-info
writing example.egg-info/PKG-INFO
writing dependency_links to example.egg-info/dependency_links.txt
writing top-level names to example.egg-info/top_level.txt
writing manifest file 'example.egg-info/SOURCES.txt'
reading manifest file 'example.egg-info/SOURCES.txt'
writing manifest file 'example.egg-info/SOURCES.txt'
/tmp/pdm-build-env-6yfs7rua-shared/lib/python3.7/site-packages/setuptools/config/pyprojecttoml.py:102: _ExperimentalProjectMetadata: Support for project metadata in `pyproject.toml` is still experimental and may be removed (or change) in future releases.
  warnings.warn(msg, _ExperimentalProjectMetadata)
running sdist
running egg_info
writing example.egg-info/PKG-INFO
writing dependency_links to example.egg-info/dependency_links.txt
writing top-level names to example.egg-info/top_level.txt
reading manifest file 'example.egg-info/SOURCES.txt'
writing manifest file 'example.egg-info/SOURCES.txt'
running check
/tmp/pdm-build-env-6yfs7rua-shared/lib/python3.7/site-packages/setuptools/config/pyprojecttoml.py:102: _ExperimentalProjectMetadata: Support for project metadata in `pyproject.toml` is still experimental and may be removed (or change) in future releases.
  warnings.warn(msg, _ExperimentalProjectMetadata)
warning: check: missing required meta-data: url

warning: check: missing meta-data: if 'author' supplied, 'author_email' should be supplied too

creating example-0.1.0
creating example-0.1.0/example
creating example-0.1.0/example.egg-info
copying files to example-0.1.0...
copying README.md -> example-0.1.0
copying pyproject.toml -> example-0.1.0
copying setup.py -> example-0.1.0
copying example/__init__.py -> example-0.1.0/example
copying example.egg-info/PKG-INFO -> example-0.1.0/example.egg-info
copying example.egg-info/SOURCES.txt -> example-0.1.0/example.egg-info
copying example.egg-info/dependency_links.txt -> example-0.1.0/example.egg-info
copying example.egg-info/top_level.txt -> example-0.1.0/example.egg-info
Writing example-0.1.0/setup.cfg
Creating tar archive
removing 'example-0.1.0' (and everything under it)
Built sdist at /home/roey/py-example/dist/example-0.1.0.tar.gz
Building wheel...
Preparing isolated env for PEP 517 build...
Reusing shared build env: /tmp/pdm-build-env-6yfs7rua-shared
running egg_info
writing example.egg-info/PKG-INFO
writing dependency_links to example.egg-info/dependency_links.txt
writing top-level names to example.egg-info/top_level.txt
reading manifest file 'example.egg-info/SOURCES.txt'
writing manifest file 'example.egg-info/SOURCES.txt'
/tmp/pdm-build-env-6yfs7rua-shared/lib/python3.7/site-packages/setuptools/config/pyprojecttoml.py:102: _ExperimentalProjectMetadata: Support for project metadata in `pyproject.toml` is still experimental and may be removed (or change) in future releases.
  warnings.warn(msg, _ExperimentalProjectMetadata)
Collecting wheel (from -r /tmp/pdm-build-reqs-n4o8d7dz.txt (line 1))
  Cache entry deserialization failed, entry ignored
  Cache entry deserialization failed, entry ignored
  Downloading https://files.pythonhosted.org/packages/27/d6/003e593296a85fd6ed616ed962795b2f87709c3eee2bca4f6d0fe55c6d00/wheel-0.37.1-py2.py3-none-any.whl
Installing collected packages: wheel
  The script wheel is installed in '/tmp/pdm-build-env-q_lud6s1-overlay/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed wheel-0.37.1
running bdist_wheel
running build
running build_py
creating build
creating build/lib
creating build/lib/example
copying example/__init__.py -> build/lib/example
copying example/generated.py -> build/lib/example
running egg_info
writing example.egg-info/PKG-INFO
writing dependency_links to example.egg-info/dependency_links.txt
writing top-level names to example.egg-info/top_level.txt
reading manifest file 'example.egg-info/SOURCES.txt'
writing manifest file 'example.egg-info/SOURCES.txt'
installing to build/bdist.linux-aarch64/wheel
running install
running install_lib
creating build/bdist.linux-aarch64
creating build/bdist.linux-aarch64/wheel
creating build/bdist.linux-aarch64/wheel/example
copying build/lib/example/__init__.py -> build/bdist.linux-aarch64/wheel/example
copying build/lib/example/generated.py -> build/bdist.linux-aarch64/wheel/example
running install_egg_info
Copying example.egg-info to build/bdist.linux-aarch64/wheel/example-0.1.0-py3.7.egg-info
running install_scripts
creating build/bdist.linux-aarch64/wheel/example-0.1.0.dist-info/WHEEL
creating '/home/roey/py-example/dist/tmpig4zi9nz/example-0.1.0-py3-none-any.whl' and adding 'build/bdist.linux-aarch64/wheel' to it
adding 'example/__init__.py'
adding 'example/generated.py'
adding 'example-0.1.0.dist-info/METADATA'
adding 'example-0.1.0.dist-info/WHEEL'
adding 'example-0.1.0.dist-info/top_level.txt'
adding 'example-0.1.0.dist-info/RECORD'
removing build/bdist.linux-aarch64/wheel
/tmp/pdm-build-env-6yfs7rua-shared/lib/python3.7/site-packages/setuptools/config/pyprojecttoml.py:102: _ExperimentalProjectMetadata: Support for project metadata in `pyproject.toml` is still experimental and may be removed (or change) in future releases.
  warnings.warn(msg, _ExperimentalProjectMetadata)
Built wheel at /home/roey/py-example/dist/example-0.1.0-py3-none-any.whl
```

And the final wheel includes `generated.py` and not `header.h` as expected :).
