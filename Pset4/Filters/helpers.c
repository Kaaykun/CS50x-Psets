#include "helpers.h"
#include "math.h"
#include "stdio.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculate average of the 3 RGB values and equalize them to create matching shades of gray
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculate RGB values of each color type Red, Green and Blue using the given formula
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            //Limit RGB values to not be higher than 255
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    //Create temp copy of the image to store as a buffer
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    //Replace the last pixel of the original with the first pixel of the temp
    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][width - 1 - l] = temp[k][l];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            //Variable for counting the number of neighbouring pixels
            int counter = 0;
            //Variables for storing the total of all neighbouring RGB values
            float totalRed = 0, totalGreen = 0, totalBlue = 0;
            //Initialize an array of coordinates of a 3x3 grid
            int rowCoord[] = {row - 1, row, row + 1};
            int colCoord[] = {col - 1, col, col + 1};

            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    //Create variables to define the current pixels location in the array
                    int currentRow = rowCoord[k];
                    int currentCol = colCoord[l];

                    if (currentRow >= 0 && currentRow < height && currentCol >= 0 && currentCol < width)
                    {
                        //Create structure to store created pixel location and enable .rgbt calls
                        RGBTRIPLE pixel = image[currentRow][currentCol];

                        counter++;
                        totalRed += pixel.rgbtRed;
                        totalGreen += pixel.rgbtGreen;
                        totalBlue += pixel.rgbtBlue;
                    }
                }
            }
            temp[row][col].rgbtRed = round(totalRed / counter);
            temp[row][col].rgbtGreen = round(totalGreen / counter);
            temp[row][col].rgbtBlue = round(totalBlue / counter);
        }
    }


    //Overwrite original image with blured version
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}