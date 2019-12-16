import os
import time

__author__ = 'Sergio Masa Avis'
import sensor_api
import pandas as pd


def main():


    path,path1,path2,path3,path4,tipo_excel = sensor_api.init()




    if(tipo_excel=='1'):
        print("Linea ozono elegida")
        data = sensor_api.load_data_linea_ozono(path)
        gas=2
        print(data)

    elif(tipo_excel=='2'):
        print("Linea wiinose elegida")
        data = sensor_api.load_data_linea_wiinose(path)
        gas=1
        print(data)
    else:
        print("Tipo de archivo incorrectamente introducido. Por favor, introduce 1 o 2")

    respuestas,Respuestas,Index = sensor_api.calcular_respuestas(data)
    sensor_api.export_excel(data,Respuestas, Index,path1)

    sensor_api.plot_all(data,respuestas,path4,tipo_excel)
    end = time.time()
    print("Duración del programa: " + str(end - start) + " segundos")




if __name__ == "__main__":
    start = time.time()
    main()