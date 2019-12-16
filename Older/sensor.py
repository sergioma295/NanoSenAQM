
# Librerías
import os
import time
import api_excel
import api_excel_
import api_caracteristicas
import sys
import argparse


__author__ = 'Sergio Masa Avis'


def get_data(Input,Output,Type):
    """ Read data from Time .xlsx file. Check type of folder and after that calls the corresponding method for storing that data.

    :type Input: str
    :param Input: Path to input folder

    :type Output: str
    :param Output:

    :type Type: int
    :param Type: Type of folder (1-Wiinose line, 2-Ozone line (with electrometer).\n\n

    :return: Data Read

    :rtype: tuple {DataFrame, list}\n
            1. DataFrame -> Data read
            2. list -> Name of gases

    """
    if(Type=='1'):
            print("[INFO] Linea: Wiinose")
            data = api_excel.extraer_datos_linea_wiinose(Input,Output)
            print(data)

    elif(Type=='2'):
        print("[INFO] Linea: Ozono")
        print("[INFO] Aún no implementado")
        sys.exit()
        # data = api_excel.extraer_datos_linea_wiinose(Input,Output)
        # print(data)

    else:
        print("[INFO] Error. Linea elegida incorrectamente")
        print("\n------------------------------------------------------------------------------\n")

    return data



def main():
    """
    Main function of python script. Steps:\n
    1) Create file folders
    2) Get data from file folder
    3) Get charactheristics of data.
    4) Save to .xlsx data generated
    """
    print("\n------------------------------------------------------------------------------")
    print("--------------------------------- BIENVENIDO ---------------------------------")
    print("------------------------------------------------------------------------------")


    # Inicialización del fichero original
    path_origen,path_destino,path_folder,path_output,path_excel,path_images, tipo_medida, path_fichero_medida = api_excel.init()

    # Obtención de datos del fichero original
    data,name_gases = get_data(Input=path_fichero_medida, Output=path_output,Type=tipo_medida)

    # Obtención del sample time
    sample_time, sample_time_mean = api_caracteristicas.get_sample_time(Data=data)
    Características = api_caracteristicas.get_characteristics(Data=data, Gases = name_gases, Sample_Time = sample_time_mean,Path = path_images)


    # Guardamos en un archivo .xlsx
    for index in range(len(Características)):
        if(Características[index]!=0):
            api_excel.procesar_caracteristicas(Características[index],path_output,name_gases[index])
        else:
            continue



if __name__ == "__main__":
    start = time.time()
    main()