import re
from zipfile import ZipFile

class DatavyuFile:
    def __init__(self, filename):
        self.zip = ZipFile(filename)
        dvf = self.zip.open("db", 'r')
        db_lines = dvf.readlines()
        dvf.close()
        self.columns = self.parse_db(db_lines)

    def parse_db(self, lines):
        last_variable = []
        columns = []
        for line in lines[1:]:
            if len(line) > 0 and not line[0].isdigit():
                if len(last_variable) > 0:
                    col = Column(last_variable)
                    columns.append(col)
                    last_variable = [line]
                else:
                    last_variable.append(line)
            elif len(line) > 0:
                last_variable.append(line)
        if len(last_variable) > 0:
            columns.append(Column(last_variable))
        for c in columns:
            print c
            for e in c.cells:
                print e


class Column:
    def __init__(self, lines):
        header = lines[0]
        self.name = header.split(" ")[0]
        header = header[len(self.name):]
        self.type = header.split(",")[0][2:]
        header = header[len(header.split("-")[0])+1:]
        self.arguments = map(lambda x: x.split("|")[0], header.split(","))
        self.cells = []
        for line in lines[1:]:
            if len(line) > 0:
                self.cells.append(Cell(line, self.arguments))

    def __str__(self):
        return self.name + " " + self.type + " " + ",".join(self.arguments)


class Cell:
    def __init__(self, line, arguments):
        line_sp = line.split(",")
        self.start = timestamp_to_ms(line_sp[0])
        self.end = timestamp_to_ms(line_sp[1])
        self.values = re.split(r"[()]", line)[1].split(",")
        self.arguments = arguments

    def __str__(self):
        return " ".join([str(self.start), str(self.end), ",".join(self.values)])

def timestamp_to_ms(ts):
    ts_sp = ts.split(":")
    hours = int(ts_sp[0]) * 60 * 60 * 1000
    minutes = int(ts_sp[1]) * 60 * 1000
    seconds = int(ts_sp[2]) * 1000
    ms = int(ts_sp[3])
    return hours + minutes + seconds + ms
