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

For Homework 2:
1. `21PyBouncingBall`: codes for drawing a bouncing ball restricted in a well.
2. Including
    - `22PyCollision`: codes simulating collisions between several balls.
    - (Extra) `22PyGravity`: codes simulating collisions between several balls considering the gravity, which is more complicated than the previous one.
3. `23PyMouseMaze`: codes for an interactive maze game. Size of the maze, say `N` and `M` should be given in comand line arguments. An example to invoke this program is `./main.py 10 10`. Use `w` and `s` to pull the mouse forwards and backwards, and use `a` and `d` to turn it counter-clock-wise and clock-wise respectively. The maze generation algorithm is slightly different from `13PyMaze`.

For Homework 3:
1. `30Report`: LaTeX source codes and .pdf files of the report of Homework 3. Note that some symbolic calculations, which are not necessary, are carried in `Problem1.ipynb`, which needs SymPy and Jupyter Notebook to run.

For Homework 4:
1. `41HalfAngleReport`: LaTeX source codes and .pdf files for Homework 4 Problem 1.
2. `42Gouraud`: codes for flat shading and Gouraud shading. Iterations of sub-division `N` should be given in command line arguments as `./main.py 2`, which should not ever exceed 6. You may use 1 or 2 to investigate details of different shading methods, and use 5 or 6 to observe global visual effects. You may tap W, A, S and D to move the view point, and tap H, J, N, M to rotate the light source. Ambient, diffuse and specular lights are set to be red, blue and green respectively. Shading methods of the four polyhedra are listed below.
    - First from left: direct flat shading, where a triangle is colored according to one vertex and the surface normal.
    - Second from left: interpolated flat shading, where a triangle is colored according to three vertices and the surface normal, with color interpolation.
    - Third from left: Gouraud shading, where a triangle is colored according to three vertices and approximated (averaged) point normals, with color interpolation.
    - Fourth from left: interpolated smooth shading using true point normals, where a triangle is colored according to three vertices and true point normals, with color interpolation. This makes advantage of properties of the sphere, normals of which can be directly calculated.
Note that some strange pattern may occur when `N` is rather large, this is because the subdivision process does not guarantee convexity.

For Homework 5:
1. `50Report`: LaTeX source codes and .pdf files for Homework 5.
2. `53LineSegment`: codes drawing a line segment using Bresenham's algorithm. Usage of the program can be seen by executing `./main.py -h`. Note that two endpoints of the line segment are all drawn, and the centers of pixels (emulated) are all integers and a half.
3. `54Circle`: codes drawing a circle using Bresenham's algorithm. Usage can also be retrieved by `/main.py -h` Centers of pixels (emulated) are all integers and a half.

## Guide to Python source files

The Python source files are all directly executable. That is, they can be directly invoked by `./main.py`.

To establish a environment, please follow the following instructions:
1. Make sure you have GCC and G++ installed on your system.
2. Install a Anaconda from [Official Website](https://www.anaconda.com/download/). The direct download link is [this](https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh).
3. Create a new Anaconda environment by `conda create -n graphics`.
4. Activate the environment by `source path/to/anaconda/bin/activate graphics`.
5. Install packages by `conda install python numpy scipy pip`.
6. Install packages by `conda install freeglut`.
7. Install packages by `pip install PyOpenGl PyOpenGL-accelerate`.
8. Change the directory and directly run the Python programs by `./main.py`.
If an Anaconda environment has already been established, the first two steps can be left out.

To install SymPy and Jupyter Notebook, (which are intended for verification of symbolic results and are not required), one may use `conda install jupyter sympy`.

## Guide to C++ source files

CMake files are affiliated for each sub-project, and you may use CMake to construct the project. The library [GLFW](http://www.glfw.org/) and [GLM]() are used in most cases.
