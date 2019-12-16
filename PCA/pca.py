import os.path
import colored
from colored import stylize
import pandas as pd
import csv

class Sensor():
    """ Sensor class.

    *** Note: You never call this class before create a file object.***

    """

    def __init__(self, SensorName, SensorID, SensorPath,GasName,GasID,GasPath ):
        self.SensorName =  SensorName
        self.SensorID = SensorID
        self.SensorPath = SensorPath
        self.GasName = GasName
        self.GasID = GasID
        self.GasPath = GasPath

    def getSensorName(self):
        return self.SensorName

    def getSensorID(self):
        return self.SensorID

    def getSensorPath(self):
        return self.SensorPath

    def getGasName(self):
        return self.GasName

    def getGasID(self):
        return self.GasID

    def getGasPath(self):
        return self.GasPath

    def setWriterCSV(self, dataset_writer):
        self.dataset_writer = dataset_writer

    def getWriterCSV(self):
        return self.dataset_writer

    def getCharacteristics(self):
        print("[INFO] Gas Path: ", self.GasPath)
        gasN_ = self.GasPath.split('/')
        gasN_ = gasN_[len(gasN_) - 1].split('.xlsx')[0]
        # Open Book and sheet
        xl = pd.ExcelFile(self.GasPath)
        sheet = xl.parse('Caracteristicas')
        # Get Data from sheet
        cycle = sheet["Ciclo"].tolist()
        respS1 = sheet["Respuesta_S1"].tolist()
        respS2 = sheet["Respuesta_S2"].tolist()
        respS3 = sheet["Respuesta_S3"].tolist()
        respS4 = sheet["Respuesta_S4"].tolist()
        hum = sheet["Humedad"].tolist()
        m1s1 = sheet["M1_S1"].tolist()
        m2s1 = sheet["M2_S1"].tolist()
        m3s1 = sheet["M3_S1"].tolist()
        m1s2 = sheet["M1_S2"].tolist()
        m2s2 = sheet["M2_S2"].tolist()
        m3s2 = sheet["M3_S2"].tolist()
        m1s3 = sheet["M1_S3"].tolist()
        m2s3 = sheet["M2_S3"].tolist()
        m3s3 = sheet["M3_S3"].tolist()
        m1s4 = sheet["M1_S4"].tolist()
        m2s4 = sheet["M2_S4"].tolist()
        m3s4 = sheet["M3_S4"].tolist()
        v1 = sheet["V1"].tolist()
        v2 = sheet["V2"].tolist()
        v3 = sheet["V3"].tolist()
        v4 = sheet["V4"].tolist()
        concentration = sheet[gasN_].tolist()
        # Save Data S1
        s1 = self.saveData(1,cycle,hum,respS1,m1s1,m2s1,m3s1, v1,concentration)
        self.updateCSV(s1)
        # Save Data S2
        s2 = self.saveData(2,cycle,hum,respS2,m1s2,m2s2,m3s2, v2,concentration)
        self.updateCSV(s2)
        # Save Data S3
        s3 = self.saveData(3,cycle,hum,respS3,m1s3,m2s3,m3s3, v3,concentration)
        self.updateCSV(s3)
        # Save Data S4
        s4 = self.saveData(4,cycle,hum,respS4,m1s4,m2s4,m3s4, v4,concentration)
        self.updateCSV(s4)

        return s1,s2,s3,s4

    def saveData(self,numSensor,cycle,humidity,response, m1, m2, m3, v_heater,concentration):
        Measure = {'SensorID': self.SensorID, 'SensorNum':numSensor,
                   'Cycle': cycle,
                   'Humidity': humidity,
                   'Response':response,
                   'M1':m1,'M2':m2,'M3':m3,
                   'V':v_heater,
                   "GasID": self.GasID,
                   'Concentration': concentration,}
        Measure = pd.DataFrame(Measure, columns=['SensorID', 'SensorNum', 'Cycle','Humidity','Response', 'M1', 'M2', 'M3', 'V', 'GasID', 'Concentration'])
        return Measure

    def updateCSV(self, sensor):
        sensorID      = sensor['SensorID'].tolist()
        sensorNum     = sensor['SensorNum'].tolist()
        cycle         = sensor['Cycle'].tolist()
        hum           = sensor['Humidity'].tolist()
        response      = sensor['Response'].tolist()
        m1            = sensor['M1'].tolist()
        m2            = sensor['M2'].tolist()
        m3            = sensor['M3'].tolist()
        vHeater       = sensor['V'].tolist()
        gasID         = sensor['GasID'].tolist()
        concentration = sensor['Concentration'].tolist()


        for i in range(len(sensorID)):
            if response[i] < 1.1:
                print("[INFO] Response not saved due to is too low")
                continue
            else:
                self.getWriterCSV().writerow([sensorID[i], sensorNum[i], cycle[i],hum[i],response[i],m1[i],m2[i],m3[i],vHeater[i],gasID[i],concentration[i]])

def getDirectories(path="../Data"):

    if(os.path.exists(path)):
        print("[INFO] Directories on path: ", path)
        files = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in dirs:
                files.append(os.path.join(root, name))

        directories = []
        for dir in range(len(files)):
            for name in os.listdir(files[dir]):
                directories.append(os.path.join(files[dir], name))

        dataChar = [] # Data Caracteris path
        dataMeas = [] # Data Measure path
        for d in range(len(directories)):
            for name in os.listdir(directories[d]):
                if name == "Datos_Procesados":
                    dataId = os.path.join(directories[d], name)
                    for file in os.listdir(dataId):
                        if file.endswith(".xlsx"):
                            f = os.path.join(dataId, file)
                            if(("NO2" in file) or ("O3" in file)):
                                dataChar.append(f)
                            else:
                                dataMeas.append(f)
                    break
        Data = {'Measure_Data': dataMeas,'Charasteristics_Data': dataChar,}
        data = pd.DataFrame(Data, columns=['Measure_Data', 'Charasteristics_Data'])

        return data

    else:
        print("[INFO] Error file not accessible")
        exit()

def getSensors(sensorName):
    sensorID = []       # Variable para almacenar el ID del sensor
    sensorName_ = []    # Variable temporal para comprobar el nombre y su ID.
    id = 1              # ID sensor. 0 -> NumSensors(diferentes nombres)
    for i in range(len(sensorName)):    # Recorremos la lista que almacena el nombre de los sensores
        if (sensorName[i] not in sensorName_):  # Comprobamos si el nombre del sensor del indice i está almacenado en la lista temporal (sensorName_). Si no lo ésta, entonces:
            sensorName_.append(sensorName[i])   # Añadimos el nombre del sensor a la lista temporal
            sensorID.append(id)                 # Añadimos el ID a la lista sensorID
            id += 1                             # Incrementamos el valor del ID.
        else:                                   # Si el nombre del sensor ya se ha almacenado anteriormente en la lista temporal, entonces:
            for j in range(len(sensorName)):    # Recorremos la lista que almacena los nombres de los sensores.
                if sensorName[i] == sensorName[j]:  # Buscamos el índice del sensor que ya ha sido almacenado.
                    sensorName_.append(sensorName[i])   # Consultamos su nombre y lo añadimos a la lista temporal
                    sensorID.append(sensorID[j])        # Añadimos el ID que corresponde a ese índice. De esta forma tenemos el mismo ID que el almacenado anteriormente
                    break
    return sensorName, sensorID

def getGases(gasName):
    gasName_ = []   # Variable temporal para almacenar los tipos de gases
    id = 1          # Variable ID para identificar el tipo de gas
    gasID = []      # Variable para almacenar el identificador del gas.
    for i in range(len(gasName)):   # Recorremos la lista donde están almacenados todos los gases de todas las medidas (por ahora solo medidas con un gas (NO INTERFERENCIAS)).
        if gasName[i] in gasName_:  # Si el nombre del gas está en la lista temporal
            for j in range(len(gasName)):  # Recorremos la lista que almacena los nombres de los sensores.
                if gasName[i] == gasName[j]:  # Buscamos el índice del sensor que ya ha sido almacenado.
                    gasName_.append(gasName[i])  # Consultamos su nombre y lo añadimos a la lista temporal
                    gasID.append(gasID[j])  # Añadimos el ID que corresponde a ese índice. De esta forma tenemos el mismo ID que el almacenado anteriormente
                    break
        else:
            gasName_.append(gasName[i])         # Añadimos el nombre del gas a la lista temporal
            gasID.append(id)                    # Añadimos el ID a la lista gasID
            id += 1                             # Incrementamos el valor del ID.
    return gasName_, gasID

def getDataFrame(sensorName, sensorID, sensorPath, gasName, gasID, gasPath):
    Sensors = {'SensorName': sensorName, 'SensorID': sensorID, "SensorPath":sensorPath,"GasName":gasName,"GasID":gasID,"GasPath":gasPath,}
    Sensors = pd.DataFrame(Sensors, columns=['SensorName', 'SensorID','SensorPath','GasName','GasID','GasPath'])
    return Sensors

def getVariables(data):
    sensorName = []
    sensorPath = []
    gasName = []
    gasPath = []
    for row in data.iterrows():
        file = row[1]["Charasteristics_Data"]

        # Get sensor name
        nameFile = row[1]["Measure_Data"].split("/")
        nameFile = nameFile[len(nameFile) - 1].split(".xlsx")[0]
        sensorName.append(nameFile)
        sensorPath.append(row[1]["Measure_Data"])

        # Get gas name
        nameGas = file.split("/")
        nameGas = nameGas[len(nameGas) - 1].split(".xlsx")[0].split("(")[0]
        gasName.append(nameGas)
        gasPath.append(file)

        # Read Charasteristics Data
        # xl = pd.ExcelFile(file)
        # Response = xl.parse('Caracteristicas')

    return sensorName, sensorPath, gasName, gasPath

def saveData(sensors, dataset_writer):
    for sensor in range(len(sensors['SensorName'])):
        sensor = Sensor(sensors['SensorName'][sensor], sensors ['SensorID'][sensor], sensors['SensorPath'][sensor], sensors['GasName'][sensor], sensors['GasID'][sensor], sensors['GasPath'][sensor])
        sensor.setWriterCSV(dataset_writer)
        print("**********************************************************************************************************")
        print("Sensor Name: ", sensor.getSensorName(), "|||| SensorID: ", sensor.getSensorID(), "|||| Sensor Path: ", sensor.getSensorPath())
        print("Gas Name: ", sensor.getGasName(), "|||| Gas ID: ", sensor.getGasID(), "|||| Gas Path: ", sensor.getGasPath())
        print("--------------------------------CARACTERISTICAS-----------------------------------------------------------")
        print(sensor.getCharacteristics())
