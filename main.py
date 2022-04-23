# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
from Crawler import Crawler
from datetime import date

if __name__ == '__main__':
    uDate = date(year=1901, month=1, day=1)
    vDate = date(year=2022, month=12, day=31)
    csv_filename = 'MalayalaMasam.csv'
    print(Crawler(csv_filename).process(startdate=uDate, enddate=vDate))
