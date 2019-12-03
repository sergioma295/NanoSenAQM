# Libraries
import os,shutil
import sys
import pandas as pd
import xlsxwriter


def export2Excel(data, path, name):
    """
    Create workbook in order to save data generated.

    :type data: str
    :param data: Path where original file folder is.

    :type path: str
    :param path: Path folder generated.

    :type name: str
    :param name: Path folder output inside folder generated.


    """

    path = path+name+'.xlsx'

    # Number of rows and columns in the file
    rows = data.shape[0]
    cols = data.shape[1]

    # Openning the excel file
    writer = pd.ExcelWriter(path)
    workbook = writer.book

    # Writing the data
    data.to_excel(writer, index=None,header=True,sheet_name='Datos')

    # Close book
    workbook.close()

def saveFeatures2Excel(data,path,name):
    """
    Storage of the characteristics in a .xlsx file with a certain format and with the name of the gas from which these\n
    characteristics have been obtained.\n

    :param data: Features to storage
    :type data: List

    :param path: Path to storage
    :type path: str

    :param name: Name of File generated
    :type name: str

    """

    path = path+name+'.xlsx' # Path


    Id =data[0]
    response1 = data[1]
    response2 = data[2]
    response3 = data[3]
    response4 = data[4]

    Humidity = data[5]

    M_S1 = data[6]
    M_S2 = data[7]
    M_S3 = data[8]
    M_S4 = data[9]

    V1   = data[10]
    V2   = data[11]
    V3   = data[12]
    V4   = data[13]

    GasConcentration = data[14]

    data_ = []
    title = ['Ciclo',
             'Respuesta_S1','Respuesta_S2','Respuesta_S3','Respuesta_S4',
             'Humedad',
             'M1_S1','M2_S1','M3_S1',
             'M1_S2','M2_S2','M3_S2',
             'M1_S3','M2_S3','M3_S3',
             'M1_S4','M2_S4','M3_S4',
             'V1', 'V2', 'V3','V4',
             str(name)]

    data_.append(title)
    for index_i in range(len(Humidity)):
        data_.append([(index_i+1),
                     response1[index_i], response2[index_i], response3[index_i], response4[index_i],
                     Humidity[index_i],
                     M_S1[index_i][0],M_S1[index_i][1],M_S1[index_i][2],
                     M_S2[index_i][0],M_S2[index_i][1],M_S2[index_i][2],
                     M_S3[index_i][0],M_S3[index_i][1],M_S3[index_i][2],
                     M_S4[index_i][0],M_S4[index_i][1],M_S4[index_i][2],
                     V1[index_i], V2[index_i], V3[index_i], V4[index_i],GasConcentration[index_i]])

    # We create a woorkbook in a folder
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet(name='Caracteristicas')


    for row, item in enumerate(data_):
        for col in range(len(data_[0])):
            worksheet.write(row, col, item[col])


    workbook.close()

class File():
    """
    Creates a File type object that allows you to read the data from the excel file you want to process.\n

    :param name: Name Output File
    :type name: str

    :param type: Measure Line Type
    :type type: str

    """

    def __init__(self, name, type):
        self.name         =  name
        self.type         =  type

    def createDirectories(self):

        """
           Create directories method use to create folder output.

           :type path_origen: str
           :param path_origen: Path where original file folder is.

           :type path_folder: str
           :param path_folder: Path folder generated.

           :type path_output: str
           :param path_output: Path folder output inside folder generated.

           :type path_excel: str
           :param path_excel: Path excel files output inside folder generated.

           :type path_images: str
           :param path_images: Path imgs files output inside folder generated.

           """
        self.path_origen  =  'Files/'
        self.path_destino =  'Data/' + self.name
        self.path_output  =  self.path_destino + '/Datos_Procesados/'
        self.path_excel   =  self.path_destino + '/excel/'
        self.path_images  =  self.path_destino + '/Imgs/'
        self.slopes       =  self.path_images  + 'Slopes/'
        self.slopes_s1    =  self.slopes + 'S1/'
        self.slopes_s2    =  self.slopes + 'S2/'
        self.slopes_s3    =  self.slopes + 'S3/'
        self.slopes_s4    =  self.slopes + 'S4/'

        try:

            # We create the general data directory
            os.mkdir(self.path_destino)

            # Creating the directory where the output is stored
            os.mkdir(self.path_output)

            # Creation of the directory where the excel files are stored
            os.mkdir(self.path_excel)

            # Creation of the image directory.
            os.mkdir(self.path_images)

            # Creation of the image directory with folder to store the slopes of each cycle
            os.mkdir(self.slopes)
            os.mkdir(self.slopes_s1)
            os.mkdir(self.slopes_s2)
            os.mkdir(self.slopes_s3)
            os.mkdir(self.slopes_s4)

            if (os.path.isdir(self.path_origen)):
                try:

                    files = []
                    for r, d, f in os.walk(self.path_origen):
                        for file in f:
                            if '.xlsx' in file:
                                files.append(os.path.join(r, file))

                    for f in files:
                        print("[INFO] File: ", f)
                except:
                    print("[INFO] Error moving file")

                shutil.copy(f, self.path_excel)
                self.path_file = f
                print('[INFO] File has been copied to ', self.path_excel)
            else:
                print("[INFO] Error. There is no file in the folder Files/")

            print("[INFO] Directories created correctly.\n")
            print("------------------------------------------------------------------------------\n")


        except:
            print("[INFO] Error. The directory already exists, use another filename.")
            print("\n------------------------------------------------------------------------------\n")
            exit()

    def readData(self):
        """
        Reading of the data to be processed and stored in a .xlsx file with the function of the class File <<wiinoseLine>>\n
        if the type entered by the user is 1 and <<ozoneLine>> if the type entered by the user is. The data is stored in\n
        a variable of class "data".If a suitable line type (1 or 2) is not received, the execution of the program ends \n
        and informs the user of the error.\n

        """
        if(self.type=='1'):
                print("[INFO] Linea: Wiinose")
                self.wiinoseLine()
                print(self.data)

        elif(self.type=='2'):
            print("[INFO] Linea: Ozono")
            print("[INFO] Aún no implementado")
            sys.exit()


        else:
            print("[INFO] Error. Incorrectly selected line")
            print("\n------------------------------------------------------------------------------\n")

    def wiinoseLine(self):
        """
        Get data from wiinose line and save that to "data" variable class File by means of <<export2Excel>> function.

        """

        try:
            # We extract the data from the file that generates the wiinose line.
            name_folder = self.path_file.split('/')[1].split(" ")[0]
            excel = pd.ExcelFile(self.path_file)
            main_variables = pd.read_excel(excel, sheet_name='resistencias')
            parameters = pd.read_excel(excel, sheet_name='parametros')
            # We define a list to store the names of the columns of the file generated in the Wiinose
            name_main_variables = []
            name_parametros_variables = []
            # Time
            for col in parameters.columns:
                name_parametros_variables.append(col)
            # Flow
            flow = parameters[name_parametros_variables[0]]
            # Tamb
            tamb = parameters[name_parametros_variables[1]]
            # Humidity
            humidity_ = parameters[name_parametros_variables[2]]
            humidity = []
            # Time Variables in seconds and minutes.
            timeMin = parameters[name_parametros_variables[3]]
            timeSec = []
            # Getting Time
            for index in range(len(timeMin)):
                timeSec.append(timeMin[index] * 60)
                humidity.append(humidity_[index] / 100)
            # Getting Main varibles
            for col in main_variables.columns:
                name_main_variables.append(col)
            # Resistances
            resistances = [main_variables[name_main_variables[0]], main_variables[name_main_variables[1]],
                            main_variables[name_main_variables[2]], main_variables[name_main_variables[3]]]
            # Heater Voltage
            voltages = [main_variables[name_main_variables[10]], main_variables[name_main_variables[11]],
                        main_variables[name_main_variables[12]], main_variables[name_main_variables[13]]]
            # Gases
            gases = [main_variables[name_main_variables[4]], main_variables[name_main_variables[5]]]
            # Number of measure
            measureNum = []
            for index in range(len(timeMin)):
                measureNum.append(index + 1)
            # Save Data like DataFrame
            Data = {'Id': measureNum,
                     'Tiempo_minutos': timeMin,
                     'Tiempo_segundos': timeSec,
                     'S1': resistances[0],
                     'S2': resistances[1],
                     'S3': resistances[2],
                     'S4': resistances[3],
                     name_main_variables[4]: gases[0],
                     name_main_variables[5]: gases[1],
                     name_parametros_variables[0]: flow,
                     'Tamb': tamb,
                     'Humidity': humidity,
                     name_main_variables[10]: voltages[0],
                     name_main_variables[11]: voltages[1],
                     name_main_variables[12]: voltages[2],
                     name_main_variables[13]: voltages[3],
                     }
            data = pd.DataFrame(Data, columns=['Id', 'Tiempo_minutos', 'Tiempo_segundos',
                                                'S1', 'S2', 'S3', 'S4',
                                                name_main_variables[4], name_main_variables[5],
                                                name_parametros_variables[0], 'Tamb', 'Humidity',
                                                name_main_variables[10], name_main_variables[11], name_main_variables[12], name_main_variables[13]])
            # Save File variables.
            self.gas1 = name_main_variables[4]
            self.gas2 = name_main_variables[5]
            self.data = data
            # We export the data to excel
            export2Excel(data, self.path_output, name_folder)


        except:
            print("[INFO] Error en ", self.path_file)
            exit()

    def getData(self):
        """
        Return data read from Excel File.\n
        :return: data
        :rtype:  DataFrame
        """
        return self.data

    def getPathOrigen(self):
        """
        Return Path Origen File\n
        :return: path_origen
        :rtype:  str
        """
        return self.path_origen

    def getPathFile(self):
        """
        Return Path Output File\n
        :return: path_destino
        :rtype:  str
        """
        return self.path_destino

    def getPathOutput(self):
        """
        Return Path Output File\n
        :return: path_output
        :rtype:  str
        """
        return self.path_output

    def getPathExcel(self):
        """
        Return Excel Path to save File\n
        :return: path_excel
        :rtype:  str
        """
        return self.path_excel

    def getPathImages(self):
        """
        Return Excel Path to save Imgs\n
        :return: path_images
        :rtype:  str
        """
        return self.path_images

    def getPathSlopes(self):
        """
        Return Excel Path to save Imgs Slopes\n
        :return: self.slopes, [self.slopes_s1, self.slopes_s2, self.slopes_s3, self.slopes_s4]
        :rtype:  str, [str, str,str,str]
        """
        return self.slopes, [self.slopes_s1, self.slopes_s2, self.slopes_s3, self.slopes_s4]

    def getIdGases(self):
        """
        Return Gases names\n
        :return: [Gas Name 1, Gas Name 2]
        :rtype:  [str, str]
        """
        return [self.gas1, self.gas2]



