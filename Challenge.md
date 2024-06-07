### Goal

Develop a preprocessing strategy in Python to fetch and stitch orthophotos based on geospatial queries.
Deliver these images resized to `256x256` pixels. Additionally, optimize the performance and
functionality benchmarking the throughput. Document the setup and idea behind it.

### Colab Notebook

Make sure to save this notebook by creating a copy in drive clicking in the menubar: *Changes will not be saved* -> *Save a copy in Drive*.

### Task Definition
#### 1. Required Technical Skills:
* Proficiency in Python programming.
* Knowledge of Geospatial data handling, GIS, and Coordinate Reference Systems (CRS).
* Experience with image processing libraries in Python, such as PIL or OpenCV.


#### 2. Sample Data:
The provided notebook will download a sample of 64 orthophotos which are a small subset of the full dataset. They correspond to a rectangular
region from `462000,5766000` to `469999,5773999` in EPSG:25832 CRS. Each image is a `.jp2` file with a resolution of `10000x10000` pixels.

Notice that the filenames from this dataset encode the geospatial coordinates range. For example, the filename `dop10rgbi_32_280_5659_1_nw_2021.jp2`
corresponds to latitude ranging from `280,000` to `280,999` and longitude from `5659,000` to `5659,999` in the EPSG:25832 CRS.
You will need to extract latitude and longitude from the filenames to pinpoint and retrieve the images relevant to given queries.

For this challenge please consider that the actual dataset would be much larger and not fit in memory all at once. Imagine that the images were being
retrieved over network on the fly. We encourage you to come up with ways to preprocess the data to optimize the retrieval process.


#### 3. Image Retrieval and Stitching
Implement the function `get_image(lat, long, radius)` with the following behavior:

- Fetches images based on latitude (lat), longitude (long), with each image typically covering a 1 km by 1 km area.
- The radius parameter should define an area around the point, typically up to `100` meters.
- Combine the required images together to cover the required area, especially near the boundaries of two or more images.
- Crop the images to a squared area that covers no more than the requested area.
- Resize the final stitched image to `256x256` pixels before returning it.
- Include error handling for access issues and data errors.

The function should handle missing data gracefully by stitching available images or filling gaps with blank data
where no images are available.


#### 4. Optimization and Benchmarking
The primary performance goal is to minimize the response time of the `get_image(lat, long, radius)` function. Given that reading
a single .jp2 file can take several seconds or minutes, your objective is to maximize the throughput.

To accomplish this, you are encouraged to employ any effective strategy that you see fit. Consider that while the radius parameter
remains generally fixed, the latitude and longitude parameters will vary randomly across requests.


#### 5. Documentation and Presentation
- Documentation: Clearly document the setup and include detailed installation instructions for all dependencies necessary to run your module.
- Presentation: Prepare to present your work in 15 minutes, detailing the functionality of your module, the strategies
implemented to optimize throughput, and any challenges encountered during the development process. This presentation
should effectively communicate the technical details and the usage of your module to both technical and non-technical
stakeholders. Provide any additional ideas how to improve your solution that were not required by the challenge or that
you didn't have the time to implement


### Results
The expected deliverables include:

1. The Notebook containing all steps of the implementation and results either through Colab share link or as a repository. You can share your copy of the notebook by clicking in the top right *Share* and select *visible for anyone with the link*.
2. A `README.md` file or a markdown cell in the notebook with **detailed instructions and explanations**. Feel free to replace this section with your own content.

You have **4 days** starting from the time you received the invitation to complete the challenge.
When you feel ready share the Colab Notebook with us.

**Have Fun!!**
