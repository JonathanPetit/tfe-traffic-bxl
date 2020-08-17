from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from shiftings import extractShiftings
from stats_residents import *
from stats_traffic import *
from stats_jobs import *

shiftingsOnlyRBC, shiftingsWithoutRBC, shiftingsWithRBC= extractShiftings()
statsTrafficRBC(shiftingsWithRBC)
count = 0 
count_e = 0
count_ext = 0
count_in = 0
for s in shiftingsWithRBC:
    if s.nace.division.section.name == "Administration publique":
        if s.district_home == "Région de Bruxelles-Capitale" and s.district_job =="Région de Bruxelles-Capitale":
            if s.transport == "voiture":
                count_in += 1
        elif s.district_home != "Région de Bruxelles-Capitale" and s.district_job =="Région de Bruxelles-Capitale":
            if s.transport == "voiture":
                count_ext += 1
print(count_in)
print(count_ext)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

class DistrictsWithRBC(Resource): 
    def get(self):
        districts = statsDistrictsRBC(shiftingsWithRBC)
        data = {"districts": districts}
        return jsonify(data)

class DistrictsWithoutRBC(Resource): 
    def get(self):
        districts = statsDistrictsRBC(shiftingsWithoutRBC)
        data = {"districts": districts}
        return jsonify(data)

class CitiesWithoutRBC(Resource): 
    def get(self):
        cities = statsCitiesRBC(shiftingsWithoutRBC)
        data = {"cities": cities}
        return jsonify(data)

class CitiesWithRBC(Resource): 
    def get(self):
        cities = statsCitiesRBC(shiftingsWithRBC)
        data = {"cities": cities}
        return jsonify(data)

class InCommingWorkersRBC(Resource):
    def get(self):
        resident = statsWorkers(shiftingsWithoutRBC)
        data = {"resident": resident}
        return jsonify(data)

class InCommingWorkersDistrictsRBC(Resource):
    def get(self):
        resident = statsInCommingWorkersDistricts(shiftingsWithoutRBC)
        data = {"resident": resident}
        return jsonify(data)


class InCommingWorkersQuarterRBC(Resource):
    def get(self):
        resident =  statsInCommingWorkersQuarters(shiftingsWithoutRBC)
        data = {"resident": resident}
        return jsonify(data)

class InternResidents(Resource):
    def get(self):
        resident = statsInternResidents(shiftingsOnlyRBC)
        data = {"residents": resident}
        return jsonify(data)

class InternWorkers(Resource):
    def get(self):
        resident = statsWorkers(shiftingsOnlyRBC)
        data = {"resident": resident}
        return jsonify(data)

class TransportsJobRBC(Resource):
    def get(self):
        cities = statsTransportsJobRBC(shiftingsOnlyRBC)
        data = {"cities": cities}
        return jsonify(data)

class TransportsHomeRBC(Resource):
    def get(self):
        cities = statsTransportsHomeRBC(shiftingsOnlyRBC)
        data = {"cities": cities}
        return jsonify(data)

class TrafficContribRBC(Resource):
    def get(self):
        data = statsTrafficRBC(shiftingsWithRBC)
        return jsonify(data)

        

class TrafficSocietyRBC(Resource):
    def get(self):
        data = statsTrafficSociety()
        data = {"society": data}
        return jsonify(data)

class TrafficCovoitRBC(Resource):
    def get(self):
        data = statsTrafficCovoit()
        data = {"covoit": data}
        return jsonify(data)

class JobsInComming(Resource):
    def get(self):
        jobs = statsJobs(shiftingsWithoutRBC)
        data = {"jobs": jobs}
        return jsonify(data)

class JobsIntern(Resource):
    def get(self):
        jobs = statsJobs(shiftingsOnlyRBC)
        data = {"jobs": jobs}
        return jsonify(data)

class JobsCitiesRBC(Resource):
    def get(self):
        jobs = statsJobsRBC(shiftingsWithRBC)
        data = {"jobs": jobs}
        return jsonify(data)

class JobsDistrictsRBC(Resource):
    def get(self):
        jobs = statsDistrictsTransportRBC(shiftingsWithoutRBC)
        data = {"jobs": jobs}
        return jsonify(data)

api.add_resource(DistrictsWithRBC, '/districtsWithRBC')
api.add_resource(DistrictsWithoutRBC, '/districtsWithoutRBC')
api.add_resource(CitiesWithoutRBC, '/citiesWithoutRBC')
api.add_resource(CitiesWithRBC, '/citiesWithRBC')
api.add_resource(InCommingWorkersRBC, '/inCommingWorkers')
api.add_resource(InCommingWorkersDistrictsRBC, '/inCommingWorkersDistricts')
api.add_resource(InCommingWorkersQuarterRBC, '/inCommingWorkersQuarters')
api.add_resource(InternResidents, '/internResidents')
api.add_resource(InternWorkers, '/internWorkers')

api.add_resource(TransportsJobRBC, '/transportsJobsRBC')
api.add_resource(TransportsHomeRBC, '/transportsHomeRBC')
api.add_resource(TrafficContribRBC, '/trafficContrib')
api.add_resource(TrafficSocietyRBC, '/trafficSociety')
api.add_resource(TrafficCovoitRBC, '/trafficCovoit')

api.add_resource(JobsInComming, "/jobsInComming")
api.add_resource(JobsIntern, "/jobsIntern")
api.add_resource(JobsCitiesRBC, "/jobsCitiesRBC")
api.add_resource(JobsDistrictsRBC, "/jobsDistrictsInComming")

if __name__ == '__main__':
     app.run(port='5002')