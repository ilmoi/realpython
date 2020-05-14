import csv
import os

os.chdir('/Users/ilja/Dropbox/realpython/practicing_itertools_sp500')

# do it once
with open('big_csv.csv', 'a') as f:
    writer = csv.writer(f)

    with open('sp500.csv', 'r') as rf:
        reader = csv.reader(rf)

        for row in reader:
            writer.writerow(row)

# do it many times
for i in range(30):
    with open('big_csv.csv', 'a') as f:
        writer = csv.writer(f)

        with open('sp500.csv', 'r') as rf:
            reader = csv.reader(rf)
            next(reader)  # skip headrow

            for row in reader:
                writer.writerow(row)
