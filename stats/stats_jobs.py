class Job():
    def __init__(self, name,):
        self.name = name
        self.people = 1
        self.percent = 0

    def addPeople(self):
        self.people += 1
    
    def setPercent(self, total):
        try:
            self.percent = round((self.people/total) * 100, 1)
        except ZeroDivisionError as e:
            pass
    
    def getDict(self):
        return {"name": self.name, "people": self.people, "percent": self.percent}


# jobs
def statsJobs(shiftings):
    jobs = dict()
    count_unkn = 0
    for shifting in shiftings:
        if shifting.nace.division.section.name in jobs:
            jobs[shifting.nace.division.section.name].addPeople()
        else:
            if shifting.nace.name == "":
                count_unkn += 1
            else:
                jobs[shifting.nace.division.section.name ] = Job(shifting.nace.division.section.name)
    
    jobs_list = []
    for key, value in jobs.items():
        value.setPercent(len(shiftings)-count_unkn)
        
        if value.percent > 3:
            jobs_list.append(value.getDict())

    jobs_list = sorted(jobs_list, key=lambda k: k['percent']) 
    return jobs_list

# type of transports per cities
def statsDistrictsTransportRBC(shiftings):
    jobs = dict()
    for shifting in shiftings:
        if shifting.district_home not in jobs:
        
            jobs[shifting.district_home] = {}
        if not shifting.nace.division.section.name  in jobs[shifting.district_home]:
            jobs[shifting.district_home][shifting.nace.division.section.name ] = Job(shifting.nace.division.section.name )
        else: 
            jobs[shifting.district_home][shifting.nace.division.section.name ].addPeople()

    jobs_list = []
    for key in jobs.keys():
        total = 0
        for i in jobs[key].values():
            total += i.people
       
        city = {}
        city["name"] = key
        total_other = 0
        for k, v in jobs[key].items():
            v.setPercent(total)
            if v.percent > 3:
                if k != "":
                    city[k] = v.percent
                else:
                    total_other += v.percent
            else:
                total_other += v.percent
            
        if len(city) > 1:
            city["autres"] = round(total_other,1)
            jobs_list.append(city)   
            
    return jobs_list

# type of transports per cities
def statsJobsRBC(shiftings):
    jobs = dict()
    for shifting in shiftings:
        if shifting.city_job not in jobs:
        
            jobs[shifting.city_job] = {}
        if not shifting.nace.division.section.name  in jobs[shifting.city_job]:
            jobs[shifting.city_job][shifting.nace.division.section.name ] = Job(shifting.nace.division.section.name )
        else: 
            jobs[shifting.city_job][shifting.nace.division.section.name ].addPeople()

    jobs_list = []
    for key in jobs.keys():
        total = 0
        total_unkn = 0
        if "" in jobs[key]:
            total_unkn += jobs[key][""].people
        for i in jobs[key].values():
            total += i.people
        

        if  key!="Vilvorde" and key != "Machelen (Hal-Vilvorde)" and  key != "Zaventem" and  key != "Anvers":
            city = {}
            city["name"] = key
            total_other = 0
            for k, v in jobs[key].items():
                if "" in jobs[key]:
                    v.setPercent(total- total_unkn)
                else: 
                    v.setPercent(total)
                if total > 2000:
                    if v.percent > 3:
                        if k != "":
                            city[k] = v.percent
                    else:
                        total_other += v.percent
            if len(city) > 1:
                city["autres"] = round(total_other,1)
                jobs_list.append(city)   
            
    return jobs_list