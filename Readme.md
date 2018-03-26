# Assignment of Computer Graphics - Spring 2018 @PKU

This is the repository of pppppass' assignment of *Computer Graphics* in Spring 2018 @PKU.

This is a Git repository and full commit logs can be retrieved. GnuPG signature are also included to perform verification except for some beginning commits.

## Table of Contents

The indices of homework and problems are attributed as leading digits of folders. Identifier of language (always `Py` and `Cpp`) follows.

For Homework 1:
1. `11PyFractalMountain`: codes drawing a fractal mountain, which performs random perturbation to control points of Sierpinski gasket.
2. Including
    - `12PyKochSnowflake`: codes drawing a Koch Snowflake using recursive deterministic algorithm.
    - (Extra) `12PyFractalTree`: codes drawing a pythagoras tree, or say a fractal tree, using recursive deterministic algorithm, which is described in [Bar93].
    - (Extra) `12IFSSierpinski`: codes drawing a Sierpinski gasket, using randomized iterated function system algorithm, which is described in [Bar93]. Note that the points are accumulated gradually.
    - (Extra) `12PyIFSFern`: codes drawing a fern using randomized iterated function system altorithm, which is described in [Bar93]. Note that the points are accumulated gradually.
3. `13PyMaze`: codes generating and drawing a maze. Size of the maze, say `N` and `M` should be given in command line arguments. An example to invoke this program is `./main.py 10 10`.

## Guide to Python source files

The Python source files are all directly executable. That is, they can be directly invoked by `./main.py`.

To establish a environment, please follow the following instructions:
1. Install a Anaconda from [Official Website](https://www.anaconda.com/download/). The direct download link is [this](https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh).
2. Create a new Anaconda environment by `conda create -n graphics`.
3. Activate the environment by `source path/to/anaconda/bin/activate graphics`.
4. Install packages by `conda install python numpy scipy pip`.
5. Install packages by `conda install freeglut`.
6. Install packages by `pip install PyOpenGl PyOpenGL-accelerate`.
7. Change the directory and directly run the Python programs by `./main.py`.
If an Anaconda environment has already been established, the first two steps can be left out.

## Guide to C++ source files

CMake files are affiliated for each sub-project, and you may use CMake to construct the project. The library [GLFW](http://www.glfw.org/) and [GLM]() are used in most cases.
