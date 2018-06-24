#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char* argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "n, infilename, outfilename\n");
        return 1;
    }

    // n times original size
    int n = atoi(argv[1]);

    if (n < 1 || n > 100)
    {
           fprintf(stderr, "n must be between 0 and 100\n");
           return 1;
    }

    // remember filenames
    char* infile = argv[2];
    char* outfile = argv[3];

    // open input file
    FILE* inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE* outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(bf), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(bi), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

////////////////
//DIMENSIONS


    // original dimensions
    int ogbiWidth = bi.biWidth;
    int ogbiHeightght = bi.biHeight;
    int ogpad = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;


    // new dimensiions
    bi.biWidth = bi.biWidth * n;
    bi.biHeight = bi.biHeight * n;
    int newpad =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // New Sizes

    bi.biSizeImage = ((bi.biWidth * sizeof(RGBTRIPLE)) + newpad) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(bf) + sizeof(bi);

////////////////////

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(bf), 1, outptr);


    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(bi), 1, outptr);


/////////////
//WRITING NEW DIMENSIONS

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(ogbiHeightght); i < biHeight; i++)
    {

        for (int row = 0; row < n; row ++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < ogbiWidth; j++)
            {
                for (int column = 0; column < n; column++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(triple), 1, inptr);


                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(triple), 1, outptr);

                    // move file pointer back
                    if (column != (n-1))
                        fseek(inptr, -sizeof(triple), SEEK_CUR);
                }

            }

            // skip over padding, if any
            fseek(inptr, ogpad, SEEK_CUR);
            // then add it back (to demonstrate how)
            for (int l = 0; l <= newpad -1; l++)
            {
                fputc(0x00, outptr);
            }
            // move file pointer back to the beginning
            if (row != (n-1))
                fseek(inptr, (-sizeof(RGBTRIPLE) * ogbiWidth) - ogpad , SEEK_CUR);
        }
    }
//////////////

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}