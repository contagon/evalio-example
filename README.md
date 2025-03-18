# [evalio](https://github.com/contagon/evalio) custom example

This repo provides a number of custom examples for how to extend evalio to use custom datasets and pipelines, both in C++ and python. We've attempted to make this process as simple as possible, so evalio can be extended with custom pipelines and datasets with minimal effort. Specifically, we provide examples for:
- C++ Pipeline
- Python Pipeline
- Python Rosbag Dataset
- Python Raw-data Dataset

We recommend using [scikit-core-build](https://scikit-build-core.readthedocs.io/) (what we use for evalio) to build the C++ pipeline and package it as a python module. Additionally, we are big fans of [uv](https://docs.astral.sh/uv/) as a frontend for this build process.

Once your research/project/etc is completed, we recommend opening a PR to evalio to make your custom pipelines or datasets available to all. This will increase its traction with the community (lower friction -> more likely to be used and cited!) and make them more widely available.

The TL;DR version, a custom dataset can be made via inheriting from the `Dataset` class in python only, and a custom pipeline from inheriting the `Pipeline` class in either C++ or python. These can then be made available to evalio via the `EVALIO_CUSTOM` env variable point to the python module that contains them.

## Usage

If you are using `uv`, you can build everything in this repo simply by running:
```bash
uv sync
```
and the `evalio_example` package will be built and installed in the current environment. No other dependencies are required! If using another python package manager, the following *should* do the same,
```bash
pip install -e .
``` 

Then, adding in these additional pipelines and datasets to evalio can be done using the `EVALIO_CUSTOM` environment variable with the python module containing the custom objects. Multiple modules can be comma separated. For example, to list our custom pipelines and datasets, you can run:
```bash
EVALIO_CUSTOM=evalio_example evalio ls pipelines -q
EVALIO_CUSTOM=evalio_example evalio ls datasets -q
```
(Noting that `evalio ls ...` may need to be prefixed with `uv run evalio ls ...`  if the `uv` environment is not active.) These pipelines and datasets can then be used in the same way as any other evalio pipeline or dataset.

## Finding evalio in CMake

If you are looking to add a custom pipeline, the header-only C++ library is included in the python package, and can be found via,
```cmake
find_package(evalio REQUIRED)
target_link_libraries(my_target PRIVATE evalio)
```
Alternatively, the library can be pulled via CMake's `FetchContent` module. See the [CMakeLists.txt](CMakeLists.txt) for an example.