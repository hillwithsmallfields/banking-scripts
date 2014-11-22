#!/usr/bin/python

"""Read my accounts files and try to reconcile them."""

import os.path
import glob
import csv
import decimal

# Where things are stored.

# Am I giving away sensitive information about my personal directory layout?
# Not really, it would only take an intruder moments to find it anyway.

cumulative_file_name = "~/tmp/finances-cumulative.csv"
cumulative_columns = ["Date", "Time", "Statement date",
                      "Payee" "Statement details",
                      "Category",
                      "Currency", "Account", "Money in", "Money out", "Balance",
                      "Location", "Project", "Note"]

financisto_dir = "~/Dropbox/Apps/financisto"

raw_bank_file = "~/finances/handelsbanken/latest.gnumeric"
raw_bank_csv = "~/finances/handelsbanken/latest.csv"
raw_bank_columns = ["Date",
                    "","Details",
                    "","Money out",
                    "","Money in",
                    "","Balance"]

# The cumulative data is keyed by the ISO date+time combination:
cumulative_data = {}

def read_cumulative():
    """Read my cumulative accounts file."""
    with open(os.path.expanduser(cumulative_file_name),
              'rb') as cumulative_file:
        cumulative_data_reader = csv.DictReader(cumulative_file)
        for row in cumulative_data_reader:
            date = row["Date"]
            time = row["Time"]
            cumulative_data[date + 'T' + time] = row
    
def read_financisto():
    """Read the CSV file exported by Financisto."""
    financisto_csv = sorted(glob.glob(os.path.expanduser(financisto_dir)
                                      + "/*.csv"))[-1]
    print "Reading financisto data from", financisto_csv
    with open(financisto_csv, 'rb') as financisto_file:
        first = True
        financisto_data = csv.DictReader(financisto_file)
        for row in financisto_data:
            if first:
                # financisto is putting some strange characters at the
                # start of the file, which get built into the date
                # key.  So, I can't use "date" as the key, but have to
                # get the version with the funny characters.
                for k in row:
                    if k.endswith("date"):
                        date_key = k
                first = False
            timestamp = row[date_key] + 'T' + row["time"]
            if (timestamp) not in cumulative_data:
                amount = decimal.Decimal(row['amount'])
                new_row = {"Date":row[date_key],
                            "Time":row['time'],
                            "Payee":row['payee'],
                            "Category":row['parent']+':'+row['category'],
                            "Account":row['account'],
                            "Currency":row['currency'],
                            "Location":row['location'],
                            "Project":row['project'],
                            "Note":row['note']}
                if amount < 0:
                    new_row['Money out'] = amount
                else:
                    new_row['Money in'] = amount
                cumulative_data[timestamp] = new_row

# todo: also look for groups of rows that match
def find_existing_row(isodate, money_in, money_out):
    """Find a row of cumulative data matching the parameters."""
    for key, existing_row in cumulative_data.iteritems():
        if ((("Money in" in existing_row)
             and (existing_row["Money in"] == money_in))
            or (("Money out" in existing_row)
                and (existing_row["Money out"] == money_out))):
            print "matched on amount"
            return existing_row

def read_handelsbanken():
    """Read my handelsbanken recent transactions file."""
    converter = ("ssconvert --export-type=Gnumeric_stf:stf_csv "
                 + raw_bank_file
                 + " " + raw_bank_csv)
    print "converting using", converter
    os.system(converter)
    handelsbanken_csv = os.path.expanduser(raw_bank_csv)
    print "Reading bank data from", handelsbanken_csv
    with open(handelsbanken_csv, 'rb') as handelsbanken_file:
        row_number = 0
        handelsbanken_data = csv.DictReader(handelsbanken_file,
                                            fieldnames=raw_bank_columns)
        for row in handelsbanken_data:
            if row_number > 5:
                isodate = row['Date'].replace('/','-')
                money_in_string = row['Money in']
                money_in = (decimal.Decimal(money_in_string)
                            if money_in_string != ''
                            else '')
                money_out_string = row['Money out']
                money_out = (decimal.Decimal(money_out_string)
                             if money_out_string != ''
                             else '')
                print row, isodate, money_in, money_out
                existing = find_existing_row(isodate, money_in, money_out)
            row_number += 1

def main():
    print "cumulative data is", cumulative_data
    read_financisto()
    read_handelsbanken()

if __name__ == "__main__":
    main()
