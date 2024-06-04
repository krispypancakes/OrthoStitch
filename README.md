# Coding Challenge

# Prerequisites

Python version: 3.10.12

After cloning the repo, please create a venv and install the requirements:

`python -m venv .venv`

`source .venv/bin/activate`

`pip install --upgrade pip`

`pip install -r requirements.txt`


# How to run
You find the main module with comments in `src/utils.py`. The object `OrthoLoader` takes care of 
finding the correct files to load, loading them, cropping and also plotting.

In the notebook `baseline.ipynb` you can download the data and run examples.

You can run `python src/run_baseline.py` to check the time of an example using coordinates that need 4 images to display the desired point.

# Results:
Results of running  `src/run_baseline.py` on two different machines:

Macbook Air 2020, M1, 8gb: 2.32 min

AMD Ryzen 7 5800X 8-Core: 1.27 min

# Remarks
## Loading
The actual loading of the images into memory is the bottle neck here and takes a lot of time.
Strategies for optimizing this were:
- Multiprocessing
- Threading
- Async functions
- pillow-simd instead of normal pillow
- using img.draft() to load a compressed version before loading

None of the above strategies worked as I liked or were not implemented correctly, so that the baseline version is the only working solution.
I kept `src/run_threading.py` as an example of the strategies I tried, but this also did not improve speed of loading on the setups I used.

## Improvements
Granted there would be mor time, what could be added or improved:
- speed of loading obviously 
- proper logging
- using a linter to enforce a style
- (better) error / exception handling
- tests and assertions

## The get_image() function

The function takes integers according to the file names as described in the initial notebook instead of floats as in the example function. 

## Progress

The `OrthoLoader` class has a new parameter: `bool: use_c`. This makes use of a script written in C which is 
compiled as a shared library. Code is here: `load_jpeg2000.c`. This makes use of `openjpeg`, which needs to 
be installed and possibly hinted to in compile step.
If `use_c = True` the regular loading function is swapped for a function that uses this library to load the images.

Time on the Macbook Air: 1.39 min.
