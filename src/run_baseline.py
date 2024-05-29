from utils import OrthoLoader
from time import time


def main():
    x = 464999
    y = 5767000
    radius = 100
    data_dir = "data/orthophotos/nw"

    loader = OrthoLoader(x=x, y=y, radius=radius, data_dir=data_dir)

    if len(loader.target_files) > 1:
        _map = loader.stitch_images()
    else:
        _map = loader.load_img()

    # loader.plot_map(_map, target=True)
    cropped = loader.crop_and_resize(_map)
    # loader.plot_map(cropped)

    return cropped


if __name__ == "__main__":
    time1 = time()
    main()
    duration = time() - time1
    print(f"The entire procedure took {duration/60} minutes.")
