-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find the crime report and gather information
SELECT *
  FROM crime_scene_reports
 WHERE street LIKE "Humphrey Street"
   AND year = 2021
   AND month = 7
   AND day = 28;
    -- Time of crime 10:15am, all 3 witnesses mention the bakery

-- Find the interview transcripts of the 3 witnesses for more clues
SELECT *
  FROM interviews
 WHERE transcript LIKE "%bakery%"
   AND year = 2021
   AND month = 7
   AND day = 28;
    -- Witness Ruth: Within 10min thief left in a car from parkinglot
    -- Witness Eugene: Thief withdrew money from ATM on Leggett Street
    -- Witness Raymond: Thief taking earliest flight on July 29, accomplice bought tickets, call duration less than 60 seconds

-- Follow up on leads from Ruth: Bakery security logs between 10:15 to 10:25am
SELECT *
  FROM bakery_security_logs
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND hour = 10
   AND minute > 14
   AND minute < 26;
    -- 7 cars left within that timeframe
    -- bakery_security_logs.id = 260 to 267

-- Follow up on leads from Eugene: Check for withdrawals from Legget Street ATM on Jul 28
SELECT *
  FROM atm_transactions
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND atm_location LIKE "%Leggett Street%"
   AND transaction_type LIKE "%withdraw%";
    -- 8 withdrawals on this day at this ATM
    -- atm_transactions.id = 246, 264, 266, 267, 269, 288, 313, 336

-- Follow up on leads from Raymond 1: Find earliest flight from Fiftyville on July 29
SELECT *
  FROM airports
 WHERE airports.id IN
         (SELECT destination_airport_id
            FROM flights
           WHERE year = 2021
             AND month = 7
             AND day = 29
             AND origin_airport_id = 8
        ORDER BY hour, minute LIMIT 1);
    -- Earliest flight at 08.20am to New York City

-- Follow up on leads from Raymond 2: Find flight id of above flight
SELECT id
  FROM flights
 WHERE year = 2021
   AND month = 7
   AND day = 29
   AND destination_airport_id = 4;
    -- flights.id = 36

-- Follow up on leads from Raymond 2: Check phone calls on July 28 lasting under 60 seconds
SELECT *
  FROM phone_calls
 WHERE year = 2021
   AND month = 7
   AND day = 29
   AND duration < 60;
    -- 9 different calls under 60 seconds were held that day

-- All basic information has been gathered
-- The thief can be found if:
    -- Passport number is listed as passanger in the flight
    -- Phone number was used to make a call less than 60 seconds
    -- License plate was spotted by the security logs
    -- There was a withdrawal from their bank account
SELECT *
  FROM people
 WHERE passport_number IN
        (SELECT passport_number
           FROM passengers
          WHERE flight_id = 36)
            AND phone_number IN
                (SELECT caller
                   FROM phone_calls
                  WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND duration < 60)
            AND license_plate IN
                (SELECT license_plate
                   FROM bakery_security_logs
                  WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND hour = 10
                    AND minute > 14
                    AND minute < 26)
            AND id IN
                (SELECT person_id
                   FROM bank_accounts
                  WHERE account_number IN
                        (SELECT account_number
                           FROM atm_transactions
                          WHERE year = 2021
                            AND month = 7
                            AND day = 28
                            AND atm_location LIKE "%Leggett Street%"
                            AND transaction_type LIKE "%withdraw%"));
-- Bruce is the thief

-- The accomplice can be found by:
    -- Tracking the call bruce made back to the accomplice
SELECT name
  FROM people
 WHERE phone_number=
        (SELECT receiver
           FROM phone_calls
          WHERE caller =
                (SELECT phone_number
                   FROM people
                  WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND duration < 60
                    AND name LIKE "Bruce"));
-- Robin is the accomplice