class TransportCities():
    def __init__(self, name, transport):
        self.name = name
        self.transport = transport
        self.people = 1
        self.percent_transport = 0

    def addPeople(self):
        self.people += 1
    
    def setPercent(self, total_cities):
        self.percent_transport = round((self.people/total_cities) * 100, 1)

# type of transports per cities
def statsTransportsJobRBC(shiftings):
    cities = dict()
    for shifting in shiftings:
        if shifting.city_job not in cities:
            cities[shifting.city_job] = {}
        if not shifting.transport in cities[shifting.city_job]:
            cities[shifting.city_job][shifting.transport] = TransportCities(shifting.city_job, shifting.transport)
        else: 
            cities[shifting.city_job][shifting.transport].addPeople()

    cities_list = []
    for key in cities.keys():
        total = 0
        for i in cities[key].values():
            total += i.people
        city = {}
        city["name"] = key
        for k, v in cities[key].items():
            v.setPercent(total)
            if total > 2000:
                city[k] = v.percent_transport
        if len(city) > 1:
            cities_list.append(city)   
            
    return cities_list

# type of transports per cities
def statsTransportsHomeRBC(shiftings):
    cities = dict()
    for shifting in shiftings:
        if shifting.city_home not in cities:
            cities[shifting.city_home] = {}
        if not shifting.transport in cities[shifting.city_home]:
            cities[shifting.city_home][shifting.transport] = TransportCities(shifting.city_home, shifting.transport)
        else: 
            cities[shifting.city_home][shifting.transport].addPeople()

    cities_list = []
    for key in cities.keys():
        total = 0
        for i in cities[key].values():
            total += i.people

        city = {}
        city["name"] = key
        for k, v in cities[key].items():
            v.setPercent(total)
            if total > 2000:
                city[k] = v.percent_transport
        if len(city) > 1:
            cities_list.append(city)   
            
    return cities_list


# auto percet
def statsTrafficRBC(shiftings):
    auto = dict()
    p_out = 0
    p_in = 0
    p_intern = 0
    total_in = 0
    total_out = 0
    total_intern = 0
    distance = 0
    for shifting in shiftings:
        if shifting.district_home != "Région de Bruxelles-Capitale":
            if shifting.district_job == "Région de Bruxelles-Capitale":
                p_in += 1
                if shifting.transport == "voiture":
                    total_in += 1
            else:
                p_out += 1
                if shifting.transport == "voiture":
                    total_out += 1
        else:
            if shifting.district_job == "Région de Bruxelles-Capitale":
                p_intern += 1
                distance += shifting.distance
                if shifting.transport == "voiture":
                    total_intern += 1
            else:
                p_out += 1
                if shifting.transport == "voiture":
                    total_out += 1


    p= p_out + p_in + p_intern
    total_voiture =  total_out + total_intern + total_in

    return {"percent_v": {"in": total_in/p_in, "intern": total_intern/p_intern, "out": total_out/p_out}, "percent_contrib": {"in": total_in/total_voiture, "intern": total_intern/total_voiture, "out": total_out/total_voiture}}

def statsTrafficSociety():
    n = 86800
    v_society_in = n*30.4/100
    v_society_ext = n*59.3/100
    v = 321000

    v_in_1 = v_society_in/100
    v_in_5 = v_society_in*5/100
    v_in_10 = v_society_in*10/100
    v_in_25 = v_society_in*25/100
    v_in_50 = v_society_in*50/100

    v_ext_1 = v_society_ext/100
    v_ext_5 = v_society_ext*5/100
    v_ext_10 = v_society_ext*10/100
    v_ext_25 = v_society_ext*25/100
    v_ext_50 = v_society_ext*50/100

    v_gain_1 = ((v_ext_1 + v_in_1)/v)*100
    v_gain_5 = ((v_ext_5 + v_in_5)/v)*100
    v_gain_10 = ((v_ext_10 + v_in_10)/v)*100
    v_gain_25 = ((v_ext_25 + v_in_25)/v)*100
    v_gain_50 = ((v_ext_50 + v_in_50)/v)*100

    return [{"percent_influent": 0, "percent_gain": 0}, {"percent_influent": 1, "percent_gain": v_gain_1}, {"percent_influent": 5, "percent_gain": v_gain_5}, {"percent_influent": 10, "percent_gain": v_gain_10}, {"percent_influent": 25, "percent_gain": v_gain_25}, {"percent_influent": 50, "percent_gain": v_gain_50}]

def statsTrafficCovoit():
    v = 88000
    v_in = v*30.4/100
    v_ext = v*59.3/100
    v_rbc = v_in + v_ext

    v_covoit_1 = (((v_rbc/100)/2)/v)*100
    v_covoit_2 = (((v_rbc*2/100)/2)/v)*100
    v_covoit_3 = (((v_rbc*3/100)/2)/v)*100
    v_covoit_5 = (((v_rbc*5/100)/2)/v)*100
    v_covoit_10 = (((v_rbc*10/100)/2)/v)*100

    return [{"percent_influent": 0, "percent_gain": 0},{"percent_influent": 1, "percent_gain": v_covoit_1}, {"percent_influent": 2, "percent_gain": v_covoit_2}, {"percent_influent": 3, "percent_gain": v_covoit_3}, {"percent_influent": 5, "percent_gain": v_covoit_5}, {"percent_influent": 10, "percent_gain": v_covoit_10}]