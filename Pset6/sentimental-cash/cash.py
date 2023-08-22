# TODO

def main():

    # List of coins available
    coins = [0.25, 0.10, 0.05, 0.01]
    # Tracker for amount of coins used
    result = 0
    change = get_change()

    # Iterate over each coin size and check if it can be used
    # Add +1 to result if coin is used and substract coin size from change
    while change >= coins[0]:
        change = round(change - coins[0], 2)
        result += 1
    while change >= coins[1]:
        change = round(change - coins[1], 2)
        result += 1
    while change >= coins[2]:
        change = round(change - coins[2], 2)
        result += 1
    while change >= coins[3]:
        change = round(change - coins[3], 2)
        result += 1

    print(result)


def get_change():
    # Get user input as float, repromt if non-float is entered
    while True:
        try:
            change = float(input("Change owed: $"))
            if change > 0:
                break
        except ValueError:
            print("That's not a float!")
    return change


main()