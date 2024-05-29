"""
Helper and utiliy functions
"""
import numpy as np
from PIL import Image
from typing import List, Union, Optional
import os
import matplotlib.pyplot as plt


class OrthoLoader:
    def __init__(self, x: int, y: int, radius: int, data_dir: str) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.data_dir = data_dir
        self.file_names = sorted(os.listdir(data_dir))

        # determine the available range in our data and check if the desired values fit
        file_longs = [self.get_x(file_path=file_name) for file_name in self.file_names]
        file_lats = [self.get_y(file_path=file_name) for file_name in self.file_names]

        file_min_long, file_max_long = min(file_longs), max(file_longs) + 999
        file_min_lat, file_max_lat = min(file_lats), max(file_lats) + 999
        
        assert file_min_long <= x <= file_max_long, f"Longitude value should be between {file_min_long} and {file_max_long}. Actual value: {x}"
        assert file_min_lat <= y <= file_max_lat, f"Latitude value should be between {file_min_lat} and {file_max_lat}. Actual value: {y}"

        # desired area to choose files and crop image
        self.x_min_crop, self.x_max_crop = x - radius, x + radius
        self.y_min_crop, self.y_max_crop = y - radius, y + radius

        self.target_files = self.get_files()

        self.x_min_map, self.x_max_map, self.y_min_map, self.y_max_map = self.get_image_coords(self.target_files)

    def get_x(self, file_path: str) -> int:
        """Returns the starting point of longitude of an image"""
        longitude = int(file_path.split('_')[2]) * 1000
        return longitude

    def get_y(self, file_path: str) -> int:
        """Returns the starting point of latitude of an image"""
        latitude = int(file_path.split('_')[3]) * 1000
        return latitude

    def load_img(self, file_path: Optional[str] = "") -> np.array:
        if len(self.target_files) == 1:
            file_path = self.target_files[0]
        print(f"loading image {file_path}.")
        img = np.array(Image.open(file_path).convert("RGB"))
        return img
    
    def get_files(self) -> List[str]:
        # get all files for the longitudinal fit
        x_files = [file for file in self.file_names if (str(int(self.x_min_crop/1000)) in file or str(int(self.x_max_crop / 1000)) in file)]
        # from those get all the files for the latitudinal range
        target_files = [file for file in x_files if (str(int(self.y_min_crop/1000)) in file or str(int(self.y_max_crop / 1000)) in file)]
        target_files = [f"{self.data_dir}/{file}" for file in target_files]
        
        return target_files 

    def stitch_images(self) -> np.ndarray: 
        # takes 2 to 4 images and stitches them together
        map_list = []
        iterations = len(self.target_files) // 2
        for i in range(iterations):
            if self.get_x(self.target_files[i*2]) == self.get_x(self.target_files[i*2+1]):
                print("X-values are same")
                img1, img2 = self.load_img(self.target_files[i*2]), self.load_img(self.target_files[i*2+1])
                print(f"Concat files {self.target_files[i*2]} and {self.target_files[i*2+1]} along the Y-axis")
                conc_long = np.concatenate((img2, img1), axis=0)
                map_list.append(conc_long)
            else:
                print("Y-values are same")
                img1, img2 = self.load_img(self.target_files[i*2]), self.load_img(self.target_files[i*2+1])
                print(f"Concat files {self.target_files[i*2]} and {self.target_files[i*2+1]} along the X-axis")
                conc_lat = np.concatenate((img1, img2), axis=1) 
                map_list.append(conc_lat)
        if len(map_list) > 1:
            _map = np.concatenate((map_list[0], map_list[1]), axis=1)

            return _map
        
        return map_list[0]

    def get_image_coords(self, file_paths: str, ) -> tuple[int]:
        image_xs = [self.get_x(file) for file in file_paths]
        image_min_x, image_max_x = min(image_xs), max(image_xs) + 999
        image_ys = [self.get_y(file) for file in file_paths]
        image_min_y, image_max_y = min(image_ys), max(image_ys) + 999

        return image_min_x, image_max_x, image_min_y, image_max_y
    
    def crop_and_resize(self, image_array: np.ndarray) -> Image:
        # get start and end values
        x_start = (self.x_min_crop - self.x_min_map) *10
        x_end = (self.x_max_crop - self.x_min_map) * 10
        y_start = (self.y_min_crop - self.y_min_map) *10
        y_end = (self.y_max_crop - self.y_min_map) * 10

        crop = Image.fromarray(image_array[y_start:y_end, x_start:x_end])
        crop = crop.resize((256,256))

        return crop

    def plot_map(self, image: Union[np.ndarray, Image.Image], target: bool = False) -> None:
        if not target: 
            plt.imshow(image)
            plt.axis("off")
            plt.show()
        else:
            plt.imshow(image, extent=[self.x_min_map, self.x_max_map, self.y_min_map, self.y_max_map])
            plt.xticks(rotation=45)

            # Marking the specific axis values
            plt.axhline(y=self.y_min_crop, color='blue', linestyle='--', label=str(self.y_min_crop))
            plt.axhline(y=self.y_max_crop, color='blue', linestyle='--', label=str(self.y_max_crop))
            plt.axvline(x=self.x_min_crop, color='green', linestyle='--', label=str(self.x_min_crop))
            plt.axvline(x=self.x_max_crop, color='green', linestyle='--', label=str(self.x_max_crop))

            # Drawing a red point
            plt.scatter(self.x, self.y, color='red', s=10)

            # Drawing a red rectangle
            rect = plt.Rectangle((self.x_min_crop, self.y_min_crop), self.x_max_crop - self.x_min_crop, self.y_max_crop - self.y_min_crop,
                                linewidth=1, edgecolor='red', facecolor='none')
            plt.gca().add_patch(rect)

            plt.legend()

            # Display the plot
            plt.show()