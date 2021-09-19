import csv


class TxtWriter:

    def __init__(self):
        self.file = open('./results.txt', 'w')

    def write(self, item: dict):
        self.file.write(f"{item}\n")


class CSVWriter:
    def __init__(self):
        self._file = open('results.csv', 'w')
        self.writer = csv.writer(self._file)
        self._headers = None

    def write(self, item: dict):

        if self._headers is None:
            # write the header
            self.writer.writerow(list(item.keys()))

        # write the data
        self.writer.writerow(list(item.values()))
