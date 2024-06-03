from utils import get_image
from time import time


def main():
    x = 464999
    y = 5767000
    radius = 100
    data_dir = "data/orthophotos/nw"

    return get_image(x, y, radius, data_dir)


if __name__ == "__main__":
    time1 = time()
    image = main()
    # store image
    image.save("cropped_image.jpeg", mode="jpeg")
    duration = time() - time1
    print(f"The entire procedure took {duration/60} minutes.")
