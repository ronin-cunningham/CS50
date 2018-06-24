#include <stdio.h>
#include <stdlib.h>
#define SIZEOFBUFFER 512

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "only input name of image you wish to recover\n");
        return 1;
    }
    FILE *recoverfile = fopen(argv[1], "r");
    if (recoverfile == NULL)
    {
        fprintf(stderr, "unable to open file\n");
        return 2;
    }

    int number_of_files = 0;
    int number_of_jpegs = 0;
    FILE *pic = NULL;
    unsigned char buffer [SIZEOFBUFFER];



    while (fread(buffer, SIZEOFBUFFER, 1, recoverfile) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            if (number_of_jpegs == 1)
            {

                fclose(pic);

            }
            else
            {
                number_of_jpegs = 1;

            }
            char filename[8];
            sprintf (filename, "%03i.jpg", number_of_files);
            pic = fopen(filename, "a");
            number_of_files +=1;
        }

        if (number_of_jpegs == 1)
        {

            fwrite(&buffer, SIZEOFBUFFER, 1, pic);
        }

    }


    fclose(pic);
    fclose(recoverfile);
    return 0;
}