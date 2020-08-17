class Distict():
    def __init__(self, name):
        self.name = name
        self.people = 1
        self.percent = 0
    
    def addPeople(self):
        self.people += 1
    
    def setPercent(self, total):
        self.percent = round((self.people/total) * 100, 1)
    
    def getDict(self):
        return {"name": self.name, "people": self.people, "percent": self.percent}

class City():
    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.people = 1
        self.percent = 0

    def addPeople(self):
        self.people += 1
    
    def setPercent(self, total):
        self.percent = round((self.people/total) * 100, 1)
    
    def getDict(self):
        return {"name": self.name, "latitude": self.lat, "longitude": self.lng, "people": self.people, "percent": self.percent}


class InCommingDistrict():
    def __init__(self, name, district):
        self.name = name
        self.district = district
        self.people = 1
        self.percent_district = 0
        self.percent_cities = 0

    def addPeople(self):
        self.people += 1
    
    def setPercent(self, total_distict, total_pers):
        self.percent_cities = round((self.people/total_distict) * 100, 1)
        self.percent_district = round((total_distict/total_pers)*100 * (self.people/total_distict), 1) 
    
    def getDict(self):
        return {"name": self.name, "district": self.district, "people": self.people, "percent_district": self.percent_district, "percent_cities": self.percent_cities }

def statsDistrictsRBC(shiftings):
    districts = dict()
    for shifting in shiftings:
        if shifting.district_home in districts:
            districts[shifting.district_home].addPeople()
        else:
            districts[shifting.district_home] = Distict(shifting.district_home)

    districts_list = []
    for key, value in districts.items():
        value.setPercent(len(shiftings))
        districts_list.append(value.getDict())

    return districts_list

# city stat residents
def statsCitiesRBC(shiftings):
    cities = dict()
    for shifting in shiftings:
        if shifting.city_home in cities:
            cities[shifting.city_home].addPeople()
        else:
            cities[shifting.city_home] = City(shifting.city_home, shifting.latitude_home, shifting.longitude_home)
    
    cities_list = []
    for key, value in cities.items():
        value.setPercent(len(shiftings))
        cities_list.append(value.getDict())
    
    return cities_list

# city stat residents in RBC
def statsInternResidents(shiftings):
    cities = dict()
    for shifting in shiftings:
        if shifting.district_home == "Région de Bruxelles-Capitale":
            if shifting.city_home in cities:
                cities[shifting.city_home].addPeople()
            else:
                cities[shifting.city_home] = City(shifting.city_home, shifting.latitude_home, shifting.longitude_home)
    
    cities_list = []
    for key, value in cities.items():
        value.setPercent(len(shiftings))
        cities_list.append(value.getDict())
    
    return cities_list


# workers 
def statsWorkers(shiftings):
    jobs = dict()
    count = 0
    for shifting in shiftings:
        if shifting.quartier_job != "":
            if shifting.quartier_job in jobs:
                jobs[shifting.quartier_job].addPeople()
            else:
                jobs[shifting.quartier_job] = City(shifting.quartier_job, shifting.latitude_job, shifting.longitude_job)
        else:
            count += 1

    jobs_list = []
    count_percent = 0
    for key, value in jobs.items():
        value.setPercent(len(shiftings)-count)
        count_percent += value.percent
        jobs_list.append(value.getDict())
    print(count_percent)
    return jobs_list


# In comming workers per districts 
def statsInCommingWorkersDistricts(shiftings):
    jobs = dict()
    for shifting in shiftings:
        if shifting.city_job not in jobs:
            jobs[shifting.city_job] = {}

        if not shifting.district_home in jobs[shifting.city_job]:
            jobs[shifting.city_job][shifting.district_home] = InCommingDistrict(shifting.city_job, shifting.district_home)
        else: 
            jobs[shifting.city_job][shifting.district_home].addPeople()

    jobs_list = []
    for key in jobs.keys():
        total = 0
        for i in jobs[key].values():
            total += i.people

        city = {}
        city["name"] = key
        for k, v in jobs[key].items():
            v.setPercent(total, len(shiftings))

            if v.percent_district  > 0.1:
                city[k] = v.percent_district
        if len(city) > 1:
            jobs_list.append(city)      
            
    return jobs_list

# In comming workers per districts 
def statsInCommingWorkersQuarters(shiftings):
    jobs = dict()
    count = 0
    for shifting in shiftings:
        if shifting.quartier_job != 0:
            if shifting.quartier_job not in jobs:
                jobs[shifting.quartier_job] = {}

            if not shifting.district_home in jobs[shifting.quartier_job]:
                jobs[shifting.quartier_job][shifting.district_home] = InCommingDistrict(shifting.quartier_job, shifting.district_home)
            else: 
                jobs[shifting.quartier_job][shifting.district_home].addPeople()
        else:
            count += 1

    jobs_list = []
    
    for key in jobs.keys():
        previous_percent = 0
        total = 0
        for i in jobs[key].values():
            total += i.people

        city = {}
        city["name"] = key
        for k, v in jobs[key].items():
            v.setPercent(total, len(shiftings)-count)


            if v.percent_cities  > previous_percent:
                city["district"] = v.district
                city["percent"] = v.percent_cities
                previous_percent = v.percent_cities
                jobs_list.append(city)      
            
    return jobs_list
    

if __name__ == "__main__":
    pass
