#include <stdio.h>
#include <openjpeg.h>
#include <time.h>

int main() {
    const char *filename = "/Users/pt/hacking/hire-me/data/orthophotos/nw/dop10rgbi_32_462_5768_1_nw_2022.jp2";
    FILE *file = fopen(filename, "rb");
    if (!file) {
        perror("Error opening file");
        return 1;
    }

    // Measure start time
    clock_t start = clock();

    // Load JPEG2000 image using OpenJPEG (example code)
    // ... (loading and decoding logic)

    // Measure end time
    clock_t end = clock();
    double time_taken = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Time taken to load JPEG2000 in C: %f seconds\n", time_taken);

    fclose(file);
    return 0;
}
