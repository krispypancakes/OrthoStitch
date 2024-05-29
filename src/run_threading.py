from utils import OrthoLoader
from time import time
import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

def load_img(file_path):
    img = Image.open(file_path).convert("RGB")
    return img

def thread_loader(file_paths: list[str]) -> list[np.ndarray]:
    n_workers = os.cpu_count()
    images = []
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(load_img, path): path for path in file_paths}
        for future in as_completed(futures):
            img = future.result()
            images.append(img)
    return images

def main():
    files = ["data/orthophotos/nw/dop10rgbi_32_462_5766_1_nw_2022.jp2", 
             "data/orthophotos/nw/dop10rgbi_32_462_5767_1_nw_2022.jp2", 
             "data/orthophotos/nw/dop10rgbi_32_462_5766_1_nw_2022.jp2", 
             "data/orthophotos/nw/dop10rgbi_32_462_5767_1_nw_2022.jp2"
             ]

    return thread_loader(files)


if __name__ == "__main__":
    time1 = time()
    main()
    duration = time() - time1
    print(f"duration: {duration/60}")
