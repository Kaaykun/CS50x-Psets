# TODO

def main():
    # Multiplication by *100 to avoid floating point inaccuracy
    denominations = [25, 10, 5, 1]

    coins = 0
    cents = get_cents()


    for i in denominations:
        count = cents // i
        cents -= count * i
        coins += count

    print(coins)


def get_cents():
    while True:
        try:
            cents = int(100*float(input("Change owed: $")))
            if cents > 0:
                break
        except ValueError:
            print("That's not a float!")
    return cents


main()