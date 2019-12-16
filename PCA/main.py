import colored as colored
import pca
import os
import pandas as pd
import csv


data_file = "../Data"
data = pca.getDirectories(data_file)
sensorName, sensorPath, gasName, gasPath = pca.getVariables(data)

sensorName, sensorID = pca.getSensors(sensorName)
gasName, gasID = pca.getGases(gasName)
sensors = pca.getDataFrame(sensorName, sensorID, sensorPath, gasName, gasID, gasPath)

with open('dataset.csv', mode='w') as dataset:
    dataset_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dataset_writer.writerow(['SensorID', 'SensorNum',
                             'Cycle', 'Humidity(%)',
                             'Response', 'M1', 'M2', 'M3',
                             'Vheater(V)',
                             'GasID','Concentration'])
    pca.saveData(sensors, dataset_writer)
