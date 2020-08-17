import csv
from utils import *

class Section():
    def __init__(self, digit, name):
        self.digit = digit
        self.name = name

class Division():
    def __init__(self, digit, name, section):
        self.digit = digit
        self.name = name
        self.section = section

class Group():
    def __init__(self, digit, name, division):
        self.digit = digit
        self.name = name
        self.division = division

class Shifting():
    def __init__(self, nace, latitude_home, longitude_home, 
                    latitude_job, longitude_job, district_home, city_home, district_job, quartier_job, city_job):
        self.nace = nace
        self.latitude_home = latitude_home
        self.longitude_home = longitude_home
        self.latitude_job = latitude_job
        self.longitude_job = longitude_job
        self.district_home = district_home
        self.city_home = city_home
        self.district_job = district_job
        self.city_job = city_job
        self.quartier_job = quartier_job
        self.distance = None
        self.transport = None
    
    def getDistance(self):
        coords_home = [float(self.latitude_home), float(self.longitude_home)]
        coords_job = [float(self.latitude_job), float(self.longitude_job)]
        self.distance = round(calculateDistance(coords_home, coords_job), 1)
    
    def getTransport(self):
        self.transport = transports(self.distance)


def extractShiftings():
    shiftings_rbc = list()
    shiftings_all = list()
    shiftings_other = list()
    with open("files/bxljobs.csv", "r") as inp:
        reader = csv.DictReader(inp, delimiter=",")
        for row in reader:
            section = Section(row["Digit Section"], row["Name Section"])
            division = Division(row["Digit Division"], row["Name Division"], section)
            group = Group(row["Digit Group"], row["Name Group"], division)
            shifting = Shifting(group, row["Latitude Residence"], row["Longitude Residence"],
                row["Latitude Job"], row["Longitude Job"], row["Province Residence"],
                row["Commune Residence"], row["Province Job"], row["Quartier Job"], row["Commune Job"])
            
            shifting.getDistance()
            shifting.getTransport()
            if row["Province Residence"] != "Région de Bruxelles-Capitale":
                shiftings_other.append(shifting)
            else:
                shiftings_rbc.append(shifting)
            shiftings_all.append(shifting)
        inp.close()
    
    return shiftings_rbc, shiftings_other, shiftings_all


if __name__ == "__main__":
    shiftings = extractShiftings()

