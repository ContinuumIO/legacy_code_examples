#include<stdio.h>
#include<math.h>

#include "image_filter.c"

main()
{
    int width, height, bpp, i, j, k, w, h, b;
    unsigned char* rgb = stbi_load( "landscape1.png", &width, &height, &bpp, 3 );
    //rgb is now three bytes per pixel, width*height size. Or NULL if load failed.

    //Raw memory for the filtered image
    unsigned char img_filtered[height][width][3];
    //Zero out the image
    for(i=0; i<height; i++){
        for(j=0; j<width; j++){
            for(k=0; k<3; k++){
                img_filtered[i][j][k] = 0;
            }
        }
    }

    apply_any_filter(rgb, (unsigned char *)img_filtered, width, height, &gaussian_filter);

    stbi_write_png("landscape_filtered_c.png", width, height, 3, img_filtered, 3*width);
    printf("done\n");
    stbi_image_free(rgb);
}
