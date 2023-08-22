import csv
from sys import argv
import sys


def main():

    # TODO: Check for command-line usage
    # Print usage if not correct and exit execution
    if len(sys.argv) != 3:
        sys.exit("Usage 'databases/xxx.csv' 'sequences/xxx.txt'.")

    # TODO: Read database file into a variable
    # Read in using "with" allows automatic closing of file
    with open(sys.argv[1], "r") as file_d:
        reader_d = csv.DictReader(file_d)
        # Initialize list for people whos STRs are listed
        people = []
        # Initialize list of all STRs
        strs = reader_d.fieldnames[1:]
        for row in reader_d:
            # Add person to list "People"
            people.append(row)

        # TODO: Read DNA sequence file into a variable
        # Read in using "with" allows automatic closing of file
        with open(sys.argv[2]) as file_s:
            # Create variable of the files content
            sequence = file_s.read()
            # Initialize dictionary for sequences using the STRs and setting them 0
            seq_count = dict.fromkeys(strs, 0)

            # TODO: Find longest match of each STR in DNA sequence
            # Loop over all STRs from the database
            for subsequence in strs:
                # Update the current STR with the value of the most amount of repeats when comparing to the sequence file
                seq_count[subsequence] = longest_match(sequence, subsequence)

            # TODO: Check database for matching profiles
            # Loop through each person in turn and check for matching STR repeats when comparing to the sequence file
            for person in people:
                match = 0
                # Loop through each STR
                for subsequence in strs:
                    # Transform the repeat value of the STR into an int
                    if int(person[subsequence]) != seq_count[subsequence]:
                        # Move to next subsequence if no match found
                        continue
                    # Update match counter if match is found
                    match += 1

                # If amounts of matches is equal to the amounts of STRs
                if match == len(strs):
                    print(person["name"])
                    sys.exit(0)
            # If no person has matchin STRs
            print("No match")
            sys.exit(1)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
