from datetime import date
from dateutil.relativedelta import relativedelta
from httplib2 import Http
from bs4 import BeautifulSoup
import csv

class Crawler:
    base_url = "https://www.prokerala.com/general/calendar/en-calendar.php"

    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def fetchpage(self, url: str):
        response, content = Http().request(uri=url, method="GET")
        if response.status == 200:
            return content
        else:
            return response.status

    def __createurl__(self, dt: date):
        return self.base_url + "?year=" + str(dt.year) + "&" + "month=" + str(dt.month)

    def parsehtml(self, month: int, year: int, response: str):
        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find(id="calendar-table")
        cells = table.find_all('div', {'class': 'day-info'})
        month_beginnings = []
        for i, cell in enumerate(cells):
            en_day = cell.parent['data-day']
            ml_day = int(cell.find('span', {'class': "sub-day"}).contents[0])
            month_ml = cell.find('span', {'class': "sub-month-name"})
            # print(en_day, ml_day, month_ml)
            if month_ml and ml_day == 1:
                month_beginnings.append((date(year=year, month=month, day=int(en_day)), month_ml.contents[0]))
        return month_beginnings

    def process(self, startdate: date, enddate: date):
        while startdate < enddate:
            url = self.__createurl__(startdate)
            content = self.parsehtml(response=self.fetchpage(url), month=startdate.month, year=startdate.year)
            print(f'{content[0][0].month}-{content[0][0].year}')
            self.csv_writer(self.csv_filename, content)
            startdate += relativedelta(months=1)

    def csv_writer(self, filename: str, table: list):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(table)
