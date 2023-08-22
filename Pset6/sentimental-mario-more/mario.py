# TODO

def main():

    height = get_height()

    for i in range(height):
        # Print right aligned pyramide
        for j in range(height):
            if j < height - i - 1:
                print(" ", end="")
            else:
                print("#", end="")
        # Print space between right and left aligned pyramide
        print("  ", end="")
        # Print left aligned pyramide
        for j in range(height):
            if j <= i:
                print("#", end="")
        # Move cursor to next line
        print()


def get_height():
    while True:
        try:
            n = int(input("Height? "))
            if ((n > 0) and (n < 9)):
                break
        except ValueError:
            print("That's not an integer!")
    return n


main()