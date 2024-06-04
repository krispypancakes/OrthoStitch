#include <stdio.h>
#include <stdlib.h>
#include <openjpeg.h>

// Structure to hold image data and properties
typedef struct {
    int width;
    int height;
    int num_components;
    unsigned char *data;
} ImageData;

// Function to load the JPEG2000 image and return pixel data
ImageData* load_jpeg2000(const char *filename) {
    // Initialize OpenJPEG decompression
    opj_dparameters_t parameters;
    opj_set_default_decoder_parameters(&parameters);

    opj_codec_t *codec = opj_create_decompress(OPJ_CODEC_JP2);
    opj_stream_t *stream = opj_stream_create_default_file_stream(filename, 1);

    opj_image_t *image = NULL;
    if (!opj_setup_decoder(codec, &parameters)) {
        fprintf(stderr, "Failed to setup decoder\n");
        return NULL;
    }

    if (!opj_read_header(stream, codec, &image)) {
        fprintf(stderr, "Failed to read header\n");
        return NULL;
    }

    if (!opj_decode(codec, stream, image)) {
        fprintf(stderr, "Failed to decode image\n");
        return NULL;
    }

    // Allocate memory for ImageData
    ImageData *img_data = (ImageData *)malloc(sizeof(ImageData));
    img_data->width = image->comps[0].w;
    img_data->height = image->comps[0].h;
    img_data->num_components = image->numcomps;

    // Allocate memory for the pixel data
    int pixel_data_size = img_data->width * img_data->height * img_data->num_components;
    img_data->data = (unsigned char *)malloc(pixel_data_size);

    // Copy image data to img_data->data
    for (int i = 0; i < pixel_data_size; i++) {
        img_data->data[i] = (unsigned char)image->comps[i % img_data->num_components].data[i / img_data->num_components];
    }

    // Clean up
    opj_destroy_codec(codec);
    opj_stream_destroy(stream);
    opj_image_destroy(image);

    return img_data;
}

// Function to free the allocated memory
void free_image_data(ImageData *img_data) {
    if (img_data) {
        if (img_data->data) {
            free(img_data->data);
        }
        free(img_data);
    }
}
