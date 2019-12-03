import time
from datetime import datetime

import api_excel
import api_sensor
import argparse
import os

from docs.conf import master_doc

__author__ = 'Sergio Masa Avis'


def init():
    """
    Initialization of the script. Check that two arguments have been passed (1- File name, 2- Type of measurement) in the script call.\n
    :return:\n
        1. name - Name of folder output
        2. type - Type of line;  1-Wiinose, 2-Electrometer

    :rtype: str, str
    """
    # Security check, run only if 2 real arguments are received
    parser = argparse.ArgumentParser(description='Program Help Guide')
    parser.add_argument('--f', metavar='Output File Name',
                        help='Enter a name for the file. E.g: python main.py --f 07-17-2019 --t 1')
    parser.add_argument('--t', metavar='Tipo de linea',
                        help='Enter the file type [1-Electrometer Line; 2-Wiinose Line]')
    args = parser.parse_args()
<<<<<<< HEAD
    args.f = "F1_1(1)"
=======
    args.f = "CNM_V4(2)"
>>>>>>> 0320fea5a7aa56c15f2e0be37345741fc267ad97
    args.t = '1'
    print("\n[INFO] File name " + args.f + " \n[INFO] Line Type: " + str(args.t))
    name = args.f
    type = args.t
    return name, type


def saveFeatures(features, path_output, name_gases):
    """
       Method that saves the characteristics in excel with a certain format by calling the function api_excel.saveFeatures2Excel.
       :type features: str
       :param features: Path where original file folder is.

       :type path_output: str
       :param path_output: Path folder generated.

       :type name_gases: str
       :param name_gases: Path folder output inside folder generated.
       """
    # Save as .xlsx
    for index in range(len(features)):
        if (features[index] != 0):
            api_excel.saveFeatures2Excel(features[index],path_output,name_gases[index])
        else:
            continue


def main():
    """
    Main function of python script. Steps:\n
    1) Create file folders
    2) Get data from file folder
    3) Get charactheristics of data.
    4) Save to .xlsx data generated
    """
    print("\n------------------------------------------------------------------------------")
    print("--------------------------------- WELCOME  -----------------------------------")
    print("------------------------------------------------------------------------------")

    # Initialization of the original file
    name, type = init()
    # Creating a File type object
    file = api_excel.File(name, type)
    # Creation of directories
    file.createDirectories()
    # Obtaining Data from the Original File
    file.readData()
    # Storing data in a variable
    # data = file.getData()
    # Creating a Measure type object
    measure = api_sensor.Measure(file)
    # Obtaining the sample time
    measure.readSampleTime()
    # Read Features
    measure.readCharacteristics()
    features = measure.getCharacteristics()
    # Save Features
    saveFeatures(features,file.getPathOutput(),file.getIdGases())




if __name__ == "__main__":
    start = time.time()
    main()