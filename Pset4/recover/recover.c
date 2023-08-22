#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>



// Define type to store a byte
typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;


void checkArgumentCount(int argc);
void checkFileExists(FILE *file);
int isJPEG(BYTE buffer[]);

int main(int argc, char *argv[])
{
    checkArgumentCount(argc);
    FILE *raw = fopen(argv[1], "r");
    checkFileExists(raw);

    // Allocate memory and initialize necessary variables
    BYTE buffer[BLOCK_SIZE];

    // Allocate buffer for the filename
    char filename[8];
    FILE *image;
    int counter = 0;

    // After JPEG image is found, all are adjacent
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, raw) == BLOCK_SIZE)
    {
        if (isJPEG(buffer) == 1)
        {
            // Close the previous image, except when it is the first JPEG
            if (counter != 0)
            {
                fclose(image);
            }
            sprintf(filename, "%03i.jpg", counter++);
            image = fopen(filename, "w");
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, image);
        }

        // Move to next block of current JPEG file and write until the next JPEG header is found
        else if (counter > 0)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, image);
        }
    }
    // Close all files
    fclose(raw);
    fclose(image);
}

// Check for correct usage of command line argument
void checkArgumentCount(int argc)
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        exit(1);
    }
}

// Make sure file has been opened
void checkFileExists(FILE *file)
{
    if (file == NULL)
    {
        printf("File could not be opened.\n");
        exit(1);
    }
}

// Check if the selected file is a JPEG image
int isJPEG(BYTE buffer[])
{
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}