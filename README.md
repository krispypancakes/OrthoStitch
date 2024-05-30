# Coding Challenge

# Prerequisites

Python version: 3.10.12

After cloning the repo, please create a venv and install the requirements:
`python -m venv .venv`
`source .venv/bin/activate`
`pip install --upgrade pip`
`pip install -r requirements.txt`

Download the data:


# Structure
You find the main module in the `src/utils.py` module. The object `OrthoLoader` takes care of 
finding the correct files to load, loading, cropping and also plotting.

You can run `python src/run_baseline.py` to check the time of an example using coordinates that need 4 images
to display the desired point.

In the notebook `baseline.ipynb` you can run this and also get plots of the initial 'big' map of 4 concatinated images,
the area we are about to cut out and the actual cropped image.