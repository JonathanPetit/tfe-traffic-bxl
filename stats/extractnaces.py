import csv
import json

from itertools import islice

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

def extractNaces():
    sections = list()
    divisions = list()
    groups = list()
    with open("files/NACEBEL_2008.csv", "r", encoding='utf-8-sig') as inp:
        reader = csv.DictReader(inp, delimiter=";")
        for row in islice(reader, 0, 384):
            if row["Code"] != '':
                if int(row["Level"]) == 1:
                    section = Section(row["Code"], row["Label FR"])
                    sections.append(section)

                elif int(row["Level"]) == 2:
                    section_parent = None
                    for section in sections: 
                        if section.digit == row["Parent code"]:
                            section_parent = section
                    
                    division = Division(row["Code"], row["Label FR"], section_parent)
                    divisions.append(division)
                
                elif int(row["Level"]) == 3:
                    division_parent = None
                    for division in divisions: 
                        if division.digit == row["Parent code"]:
                            division_parent = division
                    
                    group = Group(row["Code"], row["Label FR"], division_parent)
                    groups.append(group)
    
    return groups

def findQuartier(latitude, longitude):
    with open("files/quartier-loc.json", "r") as inp:
        data = json.load(inp)
        bestmatch = ""
        distancematch = 10
        for d in data:
            distance_lat = abs(float(d["center"][0]) - float(latitude))

            distance_lng = abs(float(d["center"][1]) - float(longitude))
            coef = distance_lat + distance_lng
            if distancematch > coef:
                bestmatch = d["name"]
                distancematch = coef
        return bestmatch



bxl_commune = ['Molenbeek-Saint-Jean', 'Woluwe-Saint-Pierre', 'Auderghem', 'Woluwe-Saint-Lambert', 'Etterbeek', 'Schaerbeek', 'Evere', 'Saint-Josse-ten-Noode', 'Bruxelles', 'Koekelberg', 'Ixelles', 'Forest (Bruxelles-Capitale)', 'Uccle', 'Saint-Gilles', 'Jette', 'Ganshoren', 'Watermael-Boitsfort', 'Berchem-Sainte-Agathe', 'Anderlecht']
def addNaces():
    naces = extractNaces()
    fieldnames = ["Digit Section", "Name Section", "Digit Division", "Name Division", "Digit Group", "Name Group", "Latitude Residence", "Longitude Residence", "Latitude Job", "Longitude Job", "Province Residence", "Commune Residence", "Province Job", "Quartier Job", "Commune Job"]
    with open("files/jobcities.csv", "r") as inp, open("files/bxljobs.csv", "w") as out:
        reader = csv.DictReader(inp, delimiter=",")
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            output_row = {}
            for nace in naces:
                if nace.digit == row["Nace"]:
                    output_row["Digit Section"] = nace.division.section.digit
                    output_row["Name Section"] = nace.division.section.name
                    output_row["Digit Division"] = nace.division.digit
                    output_row["Name Division"] = nace.division.name
                    output_row["Digit Group"] = nace.digit
                    output_row["Name Group"] = nace.name
                elif row["Nace"] == 'UNKN':
                    output_row["Digit Section"] = 'UNKN'
                    output_row["Name Section"] = 'UNKN'
                    output_row["Digit Division"] = 'UNKN'
                    output_row["Name Division"] = 'UNKN'
                    output_row["Digit Group"] = 'UNKN'
                    output_row["Name Group"] = 'UNKN'
            output_row["Latitude Residence"]= row["Latitude Residence"]
            output_row["Longitude Residence"]= row["Longitude Residence"]
            output_row["Latitude Job"]= row["Latitude Job"]
            output_row["Longitude Job"]= row["Longitude Job"]
            output_row["Province Residence"]= row["Province Residence"]
            output_row["Commune Residence"]= row["Commune Residence"]
            if row["Commune Job"] in bxl_commune:
                output_row["Province Job"] = "Région de Bruxelles-Capitale"
                output_row["Quartier Job"] = findQuartier(output_row["Latitude Job"], output_row["Longitude Job"])
            else:
                output_row["Province Job"] = "other"
                output_row["Quartier Job"] = ""
           
            output_row["Commune Job"]= row["Commune Job"]
            writer.writerow(output_row)

if __name__ == "__main__":
    addNaces()



