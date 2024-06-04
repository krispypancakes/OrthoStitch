"""
Helper and utiliy functions
"""
import ctypes
import numpy as np
from PIL import Image
from typing import List, Union, Optional
import os
import matplotlib.pyplot as plt
from time import time


libjpeg2000 = ctypes.CDLL("src/libjpeg2000.so")

class ImageData(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("num_components", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_ubyte))]


def c_load(filename: str) -> np.ndarray:
    libjpeg2000.load_jpeg2000.restype = ctypes.POINTER(ImageData)
    libjpeg2000.load_jpeg2000.argtypes = [ctypes.c_char_p]
    libjpeg2000.free_image_data.argtypes = [ctypes.POINTER(ImageData)]
    bytes_filename = filename.encode("utf-8")
    img_data_ptr = libjpeg2000.load_jpeg2000(bytes_filename)
    if not img_data_ptr:
        raise Warning("no valid pointer")
    img_data = img_data_ptr.contents
    width, height, num_components = img_data.width, img_data.height, img_data.num_components
    pixel_data = np.ctypeslib.as_array(img_data.data, shape=(height, width, num_components))
    # copy the rgb channels so that we deal with memory in python world
    img = pixel_data[:, :, :3].copy()
    # Free the image data
    libjpeg2000.free_image_data(img_data_ptr)
    print("Memory freed")
    return img


class OrthoLoader:
    def __init__(self, x: int, y: int, radius: int, data_dir: str, use_c: bool = False) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.data_dir = data_dir
        # whether or not to use the c lib to load images
        self.use_c = use_c 
        self.file_names = sorted(os.listdir(data_dir))
        # determine the available range in our data and check if the desired values fit
        file_x_vals = [self.get_x(file_path=file_name) for file_name in self.file_names]
        file_y_vals = [self.get_y(file_path=file_name) for file_name in self.file_names]
        # Determine the range of our data 
        file_min_long, file_max_long = min(file_x_vals), max(file_x_vals) + 999
        file_min_lat, file_max_lat = min(file_y_vals), max(file_y_vals) + 999
        # Make sure the request can be handled
        assert file_min_long <= x <= file_max_long, f"X value should be between {file_min_long} and {file_max_long}. Actual value: {x}"
        assert file_min_lat <= y <= file_max_lat, f"Y value should be between {file_min_lat} and {file_max_lat}. Actual value: {y}"
        # Desired area to choose files and crop image
        self.x_min_crop, self.x_max_crop = x - radius, x + radius
        self.y_min_crop, self.y_max_crop = y - radius, y + radius
        # Grab all the necessary files to display the desired point
        self.target_files = self.get_files()
        # Get coordinates of the chosen files
        self.x_min_map, self.x_max_map, self.y_min_map, self.y_max_map = self.get_image_coords(self.target_files)
        # Get start and end values for cropping; one unit of coordinate values corresponds to 10 pixels
        self.x_start = (self.x_min_crop - self.x_min_map) *10 
        self.x_end = (self.x_max_crop - self.x_min_map) * 10
        self.y_start = (self.y_max_map - self.y_max_crop) *10
        self.y_end = (self.y_max_map - self.y_min_crop) * 10

    def get_x(self, file_path: str) -> int:
        """Returns the starting point of X-value of an image"""
        longitude = int(file_path.split('_')[2]) * 1000
        return longitude

    def get_y(self, file_path: str) -> int:
        """Returns the starting point of Y-value of an image"""
        latitude = int(file_path.split('_')[3]) * 1000
        return latitude

    def load_img(self, file_path: Optional[str] = "") -> np.ndarray:
        """Returns image as Numpy array. This is the absolute bottle neck. Loading is very slow."""
        time1 = time()
        if len(self.target_files) == 1:
            file_path = self.target_files[0]
        print(f"loading image {file_path}.")
        if not self.use_c:
            img = np.asrray(Image.open(file_path).convert("RGB"))
        else:
            print("Using C speedup")
            img = c_load(file_path)
        duration = (time() - time1) / 60
        print(f"Loading the image took: {duration} min.")
        return img
    
    def get_files(self) -> List[str]:
        """Returns a list of all the file paths we need to display the desired point."""
        print("Analyzing request to extract the correct files.")
        # Get all files for the longitudinal fit
        x_files = [file for file in self.file_names if (str(int(self.x_min_crop/1000)) in file or str(int(self.x_max_crop / 1000)) in file)]
        # From those get all the files for the latitudinal range
        target_files = [file for file in x_files if (str(int(self.y_min_crop/1000)) in file or str(int(self.y_max_crop / 1000)) in file)]
        target_files = [f"{self.data_dir}/{file}" for file in target_files]
        
        return target_files 

    def stitch_images(self) -> np.ndarray: 
        """Returns the combined images as Numpy array."""
        # Takes 2 to 4 images and stitches them together
        map_list = []
        iterations = len(self.target_files) // 2
        for i in range(iterations):
            if self.get_x(self.target_files[i*2]) == self.get_x(self.target_files[i*2+1]):
                img1, img2 = self.load_img(self.target_files[i*2]), self.load_img(self.target_files[i*2+1])
                print(f"Concat files {self.target_files[i*2]} and {self.target_files[i*2+1]} along the Y-axis")
                time1 = time()
                conc_long = np.concatenate((img2, img1), axis=0)
                duration = time() - time1
                print(f"Concating two images took: {duration} sec.")
                map_list.append(conc_long)
            else:
                img1, img2 = self.load_img(self.target_files[i*2]), self.load_img(self.target_files[i*2+1])
                print(f"Concat files {self.target_files[i*2]} and {self.target_files[i*2+1]} along the X-axis")
                time1 = time()
                conc_lat = np.concatenate((img1, img2), axis=1)
                duration = time() - time1
                print(f"Concating two images took: {duration} sec.")  
                map_list.append(conc_lat)
        if len(map_list) > 1:
            _map = np.concatenate((map_list[0], map_list[1]), axis=1)

            return _map
        
        return map_list[0]

    def get_image_coords(self, file_paths: str, ) -> tuple[int]:
        """Returns the coordinates of an image(-path)."""
        image_xs = [self.get_x(file) for file in file_paths]
        image_min_x, image_max_x = min(image_xs), max(image_xs) + 999
        image_ys = [self.get_y(file) for file in file_paths]
        image_min_y, image_max_y = min(image_ys), max(image_ys) + 999

        return image_min_x, image_max_x, image_min_y, image_max_y
    
    def crop_and_resize(self, image_array: np.ndarray) -> Image:
        """Returns the cropped and resized array as PIL.Image."""
        # Cut out the desired area
        crop = Image.fromarray(image_array[self.y_start:self.y_end, self.x_start:self.x_end])
        crop = crop.resize((256,256))

        return crop

    def plot_map(self, image: Union[np.ndarray, Image.Image], target: bool = False) -> None:
        """
        Either a simple display of the image at hand or a preview of the area that is 
        supposed to be cropped, drawing a rectangle around it.
        """
        if not target: 
            plt.imshow(image)
            plt.axis("off")
            plt.show()
        else:
            plt.imshow(image, extent=[self.x_min_map, self.x_max_map, self.y_min_map, self.y_max_map])
            plt.xticks(rotation=45)

            # Marking the axis values and creating a cross to locate our target
            plt.axhline(y=self.y_min_crop, color='blue', linestyle='--', label=str(self.y_min_crop))
            plt.axhline(y=self.y_max_crop, color='blue', linestyle='--', label=str(self.y_max_crop))
            plt.axvline(x=self.x_min_crop, color='green', linestyle='--', label=str(self.x_min_crop))
            plt.axvline(x=self.x_max_crop, color='green', linestyle='--', label=str(self.x_max_crop))

            # Mark the target as red dot
            plt.scatter(self.x, self.y, color='red', s=10)

            # Mark a red rectangle around the are we want to crop
            rect = plt.Rectangle((self.x_min_crop, self.y_min_crop), self.x_max_crop - self.x_min_crop, self.y_max_crop - self.y_min_crop,
                                linewidth=1, edgecolor='red', facecolor='none')
            plt.gca().add_patch(rect)
            plt.legend()
            plt.show()

def get_image(lat: int, long: int,radius: int, dataset: str, _print: bool =False, use_c: bool = False) -> Image.Image:
    """
    Inputs to the function are integer values alligning with the file names. 
    Returns the cropped desired area as Image.
    """
    # create the loader object
    print("Initialize Loader object.")
    loader = OrthoLoader(x=lat, y=long, radius=radius, data_dir=dataset, use_c=use_c)
    # check if there is one or more images that need to be loaded to display the desired area
    if len(loader.target_files) > 1:
        _map = loader.stitch_images()
    else:
        _map = loader.load_img()
    # crop and resize the map
    cropped = loader.crop_and_resize(_map)
    
    if not _print:
        return cropped

    # show an image of the entire map with the area highlighted that is going to be cropped
    loader.plot_map(_map, target=True)
    # show the resulting image
    loader.plot_map(cropped)
    
    return cropped
