# Example

## Installing
This PDM example installs the package using `build.py` in an editable manner, **not** generating `generated.py` in-project.

`pdm/pep517/editable.py:78:88` in "pdm-pep517" repo:
```python
    def _build(self, wheel: zipfile.ZipFile) -> None:
        if self.meta.build:
            setup_py = self.ensure_setup_py()
            build_args = [
                sys.executable,
                str(setup_py),
                "build_ext",
                "--inplace",
            ]
            try:
                subprocess.check_call(build_args)
```

"build_ext" is called, "build_py" is not.

## Building
`pdm build` calls `build.py` which generates the python source file `generated.py`:
```
roey@penguin:~/py-example$ pdm build -v
Building sdist...
Preparing isolated env for PEP 517 build...
Collecting pdm-pep517>=0.12.0 (from -r /tmp/pdm-build-reqs-gsglcb64.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/7e/16/2aed2fd2d08629c7efc57157513ca9d36cfaaf7f883174ba994c6e270b21/pdm_pep517-0.12.4-py3-none-any.whl
Installing collected packages: pdm-pep517
Successfully installed pdm-pep517-0.12.4
/tmp/pdm-build-env-bso8ochl-shared/lib/python3.7/site-packages/pdm/pep517/sdist.py:53: PDMWarning: No license files are matched with glob patterns ['LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*'].
  super()._find_files_iter(for_sdist), self.find_license_files()
 - Adding build.py
 - Adding example/__init__.py
 - Adding example/header.h
 - Adding pyproject.toml
 - Adding PKG-INFO
Built sdist at /home/roey/py-example/dist/example-0.1.0.tar.gz
Building wheel...
Preparing isolated env for PEP 517 build...
Reusing shared build env: /tmp/pdm-build-env-bso8ochl-shared
Collecting setuptools>=40.8.0 (from -r /tmp/pdm-build-reqs-7zi1bmo6.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/fb/58/9efbfe68482dab9557c49d433a60fff9efd7ed8835f829eba8297c2c124a/setuptools-62.1.0-py3-none-any.whl
Installing collected packages: setuptools
Successfully installed setuptools-62.1.0
running build
running build_py
creating /home/roey/py-example/build
creating /home/roey/py-example/build/lib
creating /home/roey/py-example/build/lib/example
copying example/__init__.py -> /home/roey/py-example/build/lib/example
copying example/generated.py -> /home/roey/py-example/build/lib/example
running egg_info
creating example.egg-info
writing example.egg-info/PKG-INFO
writing dependency_links to example.egg-info/dependency_links.txt
writing top-level names to example.egg-info/top_level.txt
writing manifest file 'example.egg-info/SOURCES.txt'
reading manifest file 'example.egg-info/SOURCES.txt'
writing manifest file 'example.egg-info/SOURCES.txt'
copying example/header.h -> /home/roey/py-example/build/lib/example
/tmp/pdm-build-env-844_t_ze-overlay/lib/python3.7/site-packages/setuptools/config/pyprojecttoml.py:102: _ExperimentalProjectMetadata: Support for project metadata in `pyproject.toml` is still experimental and may be removed (or change) in future releases.
  warnings.warn(msg, _ExperimentalProjectMetadata)
/tmp/pdm-build-env-bso8ochl-shared/lib/python3.7/site-packages/pdm/pep517/wheel.py:152: PDMWarning: No license files are matched with glob patterns ['LICEN[CS]E*', 'COPYING*', 'NOTICE*', 'AUTHORS*'].
  for license_file in self.find_license_files():
 - Adding example/__init__.py
 - Adding example/header.h
 - Adding example-0.1.0.dist-info/WHEEL
 - Adding example-0.1.0.dist-info/METADATA
 - Adding example-0.1.0.dist-info/RECORD
Built wheel at /home/roey/py-example/dist/example-0.1.0-cp37-cp37m-linux_aarch64.whl
```

**But** the final wheel doesn't include `generated.py`. In fact it includes `header.h` which is unwanted.

Why?

In `pdm/pep517/wheel.py:64:77`:
```python
    def build(self, build_dir: str, **kwargs: Any) -> str:
        if not os.path.exists(build_dir):
            os.makedirs(build_dir, exist_ok=True)

        self._records.clear()
        fd, temp_path = tempfile.mkstemp(suffix=".whl")
        os.close(fd)

        with zipfile.ZipFile(
            temp_path, mode="w", compression=zipfile.ZIP_DEFLATED
        ) as zip_file:
            self._copy_module(zip_file)
            self._build(zip_file)
            self._write_metadata(zip_file)
```
The wheel is built by pdm-pep517 logic (_copy_module`) and not by setuptools by first copying python source files (implementing "build_py" logic) and then building using setuptool's "build" command (which calls "build_py" and "build_ext").
After building using setuptools, only extensions are copied as can be seen in `pdm/pep517/wheel.py:182:200`:
```python
    def _build(self, wheel: zipfile.ZipFile) -> None:
        if not self.meta.build:
            return
        setup_py = self.ensure_setup_py()
        build_args = [
            sys.executable,
            str(setup_py),
            "build",
            "-b",
            str(self.location / "build"),
        ]
        try:
            subprocess.check_call(build_args)
        except subprocess.CalledProcessError as e:
            raise BuildError(f"Error occurs when running {build_args}:\n{e}")
        build_dir = self.location / "build"
        lib_dir = next(build_dir.glob("lib.*"), None)
        if not lib_dir:
            return
```
Notice the `glob` looking for a `lib.*` pattern (extensions).
