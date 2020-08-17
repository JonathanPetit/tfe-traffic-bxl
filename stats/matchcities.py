import csv

def matchResidence(lat, lng):
    with open('files/output-cities-latlong.csv', 'r') as inp:
        reader = csv.DictReader(inp, delimiter=',')
        bestmatch = {}
        distancematch = 10
        for row in reader:
            distance_lat = abs(float(lat) - float(row["latitude"]))
            distance_lng = abs(float(lng) - float(row["longitude"]))
            coef = distance_lat + distance_lng
            if distancematch > coef:
                bestmatch = row
                distancematch = coef
        
        if bestmatch["province"] == '':
            bestmatch["province"] = 'Région de Bruxelles-Capitale'
        
        return bestmatch["province"], bestmatch["commune"], float(lat), float(lng)

def matchJob(lat, lng):
    with open('files/output-cities-latlong.csv', 'r') as inp:
        reader = csv.DictReader(inp, delimiter=',')
        bestmatch = {}
        distancematch = 10
        for row in reader:
            distance_lat = abs(float(lat) - float(row["latitude"]))
            distance_lng = abs(float(lng) - float(row["longitude"]))
            coef = distance_lat + distance_lng
            if distncematch > coef:
                bestmatch = row
                distancematch = coef
 
        return bestmatch["commune"]

def matchCities():
    fieldnames = ["Nace", "Latitude Residence", "Longitude Residence", "Latitude Job", "Longitude Job", "Province Residence", "Commune Residence", "Commune Job"]
    with open('files/jobmatching.csv', 'r') as inp, open('files/jobcities.csv', 'w') as out:
        reader = csv.DictReader(inp, delimiter=';')
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()

        previous_lat = 0
        previous_lng = 0
        province_residence = ''
        commune_residence = ''

        for row in reader:
            output_row = {}
            output_row["Nace"]= row["Nace"]
            output_row["Latitude Residence"]= row["Latitude Residence"]
            output_row["Longitude Residence"]= row["Longitude Residence"]
            output_row["Latitude Job"]= row["Latitude Job"]
            output_row["Longitude Job"]= row["Longitude Job"]

            if previous_lat == float(row["Latitude Residence"]) and previous_lng == float(row["Longitude Residence"]):
                output_row["Province Residence"]= province_residence
                output_row["Commune Residence"]= commune_residence
            else:
                province_residence, commune_residence, previous_lat, previous_lng = matchResidence(row["Latitude Residence"], row["Longitude Residence"])

            commune_job = matchJob(row["Latitude Job"], row["Longitude Job"])
            output_row["Province Residence"]= province_residence
            output_row["Commune Residence"]= commune_residence
            output_row["Commune Job"]= commune_job
            writer.writerow(output_row)