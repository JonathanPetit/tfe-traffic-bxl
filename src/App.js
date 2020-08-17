import React, { useRef, useEffect } from "react";

import district from "./geojson/belgium-districts.json";
import brussels from "./geojson/brussels.json";
import BrusselsMap from "./BrusselsMap";
import quartier from "./geojson/quartierWGS.json"

import PercentBar from "./PercentBar";
import StackedChartBar from "./StackedChartBar";
import DistrictsMap from "./DistrictsMap";
import LineChart from "./LineChart";

import { colors_districts, districts } from './map_utils.js'


function App() {
  return (
    <div>
      <LineChart
        width={1000}
        height={1000}
        url={"http://127.0.0.1:5002/trafficSociety"}
        dataset={"society"}
        >
      </LineChart>
    </div>
  )
}

export default App;

/* OK
      <LineChart
        width={1000}
        height={1000}
        url={"http://127.0.0.1:5002/trafficCovoit"}
        dataset={"covoit"}
        >
      </LineChart>
      <LineChart
        width={1000}
        height={1000}
        url={"http://127.0.0.1:5002/trafficSociety"}
        dataset={"society"}
        >
      </LineChart>
      <BrusselsMap
        width={1000}
        height={1000}
        geojson={quartier}
        url_api="http://127.0.0.1:5002/inCommingWorkers"
        dataset="resident"
        title="Lieux de travail des navetteurs entrants">
      </>
        <PercentBar
          width={1000}
          height={800}
          url={'http://127.0.0.1:5002/internResidents'}
BrusselsMap          dataset={"residents"}
          title={'Poucentage du nombre de travailleurs entrants en fonction de la province'}>
        </PercentBar>
       <PercentBar
          width={1000}
          height={800}
          url={"http://127.0.0.1:5002/jobsInComming"}
          dataset={"jobs"}
          title={'Secteurs d'activité des travailleurs entrants'}>
        </PercentBar>
        <PercentBar
          width={1000}
          height={800}
          url={"http://127.0.0.1:5002/districtsWithoutRBC"}
          dataset={"districts"}
          title={'Poucentage du nombre de travailleurs entrants en fonction de la province'}>
        </PercentBar>
      <StackedChartBar
        width={1100}
        height={700}
        url_api="http://127.0.0.1:5002/inCommingWorkersDistricts"
        colors={colors_districts}
        info={districts}>
      </StackedChartBar>

      <DistrictsMap 
          width={1000}
          height={1000}
          geojson={district}>
        </DistrictsMap>
      <BrusselsMap
        width={1000}
        height={1000}
        geojson={brussels}
        url_api="http://127.0.0.1:5002/inCommingWorkers"
        dataset="resident"
        title="Lieux de travail des navetteurs entrants">
      </BrusselsMap>
        <BrusselsMap
        width={1000}
        height={1000}
        geojson={brussels}
        url_api="http://127.0.0.1:5002/internWorkers"
        dataset="jobs"
        title="Lieux de travails des habitants interners à la RBC">
      </BrusselsMap>
*/