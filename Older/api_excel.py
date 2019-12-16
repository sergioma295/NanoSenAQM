import argparse
import os,shutil
import sys
import pandas as pd
import xlsxwriter
from matplotlib.pyplot import figure, xlabel, ylabel, show, title, legend, savefig


def init():
    """
    Init api_excel. Read the input folder .xlsx from args and type of measurment and after that, create directories if not
    exit. If directory exit, finish the execution.

    :return:\n
    1. path_origen    -> Path where original file folder is.
    2. path_destino   -> Path where output file will be saved.
    3. path_folder    -> Path folder generated.
    4. path_output    -> Path folder output inside folder generated.
    5. path_excel     -> Path excel files output inside folder generated.
    6. path_images    -> Path imgs files output inside folder generated.
    7. tipo_linea     -> Type of line (1. Wiinose, 2. Ozono).
    8. fichero_medida -> Path where original file is.


    :rtype: str, str, str, str, str, str, str, str
    """
    # Definición variables
    path_destino = 'Data/'
    path_origen = 'Ficheros/'

    # Comprobación de seguridad, ejecutar sólo si se reciben 2 argumentos reales
    parser = argparse.ArgumentParser(description='Guía de ayuda del programa')
    parser.add_argument('--f', metavar='Nombre Fichero Salida',help='Introduce un nombre para el archivo: Ej: python main.py --f 07-17-2019 --t 1')
    parser.add_argument('--t', metavar='Tipo de linea',help='Introduce el tipo de fichero [1-Linea ozono 2-Linea Wiinose]')
    args = parser.parse_args()

    args.f = "F1_1_old_3"
    args.t = '1'

    print("\n[INFO] Nombre del fichero: "+args.f+" \n[INFO] Tipo de línea: "+str(args.t))


    # Directorios
    path_folder  = path_destino+args.f
    path_output = path_folder + '/Datos_Procesados/'
    path_excel = path_folder + '/excel/'
    path_images = path_folder + '/Imgs/'

    # Línea de experimento (1-> Ozono ;2-> Wiinose)
    tipo_linea =args.t


    try:

        # Creamos los directorios
        fichero_medida = crear_directorios(path_origen,path_folder,path_output,path_excel,path_images)


        print("[INFO] Directorios creados correctamente.\n")
        print("------------------------------------------------------------------------------\n")


    except:
        print("[INFO] El directorio ya existe, utilice otro nombre de archivo")
        print("\n------------------------------------------------------------------------------\n")
        exit()





    return path_origen,path_destino,path_folder,path_output,path_excel,path_images,tipo_linea, fichero_medida

def crear_directorios(path_origen,path_folder,path_output,path_excel,path_images):
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
    # Creamos el directorio general de datos
    os.mkdir(path_folder)

    # Creación del directorio donde se almacena la salida
    os.mkdir(path_output)

    # Creación del directorio donde se guardan los excel
    os.mkdir(path_excel)

    # Creación del directorio de imagenes.
    os.mkdir(path_images)

    # Creación del directorio de imágenes con carpeta para almacenar las pendientes de cada ciclo
    os.mkdir(path_images+'Slopes')
    os.mkdir(path_images+'Slopes/S1/')
    os.mkdir(path_images+'Slopes/S2/')
    os.mkdir(path_images+'Slopes/S3/')
    os.mkdir(path_images+'Slopes/S4/')


    if (os.path.isdir(path_origen)):
        try:

            files = []
            for r, d, f in os.walk(path_origen):
                for file in f:
                    if '.xlsx' in file:
                        files.append(os.path.join(r, file))

            for f in files:
                print("[INFO] Fichero: ",f)
        except:
            print("Error moviendo el archivo")

        shutil.copy(f, path_excel)
        print('[INFO] El fichero ha sido copiado a ', path_excel)
        return f
    else:
        print("[INFO] No existe ningun archivo en la /Ficheros")

def extraer_datos_linea_wiinose(path,path_output):
    """
    Get data from wiinose line.

    :type path: str
    :param path: Path where original file folder is.

    :type path_output: str
    :param path_output: Path where the output will be saved

    :return: Data Read

    :rtype: tuple {DataFrame, list}\n
            1. DataFrame -> Data read
            2. list -> Name of gases


    """

    try:
        # Extraemos los datos del fichero que genera la línea de la wiinose.
        name_folder = path.split('/')[1].split(" ")[0]
        excel = pd.ExcelFile(path)
        main_variables = pd.read_excel(excel,sheet_name='resistencias')
        parametros = pd.read_excel(excel, sheet_name='parametros')

        # Definimos una lista para almacenar los nombres de las columnas del archivo generado en la Wiinose
        name_main_variables = []
        name_parametros_variables = []

        # TIEMPO
        for col in parametros.columns:
            name_parametros_variables.append(col)


        caudal = parametros[name_parametros_variables[0]]
        t_ambiente = parametros[name_parametros_variables[1]]
        humidity_ = parametros[name_parametros_variables[2]]
        humidity = []
        tiempo_minutos = parametros[name_parametros_variables[3]]
        tiempo_segundos = []

        for index in range(len(tiempo_minutos)):
            tiempo_segundos.append(tiempo_minutos[index] * 60)
            humidity.append(humidity_[index] / 100)



        for col in main_variables.columns:
            name_main_variables.append(col)

        # Resitencias
        resistencias = [main_variables[name_main_variables[0]], main_variables[name_main_variables[1]], main_variables[name_main_variables[2]],main_variables[name_main_variables[3]]]


        # Gases
        gases = [main_variables[name_main_variables[4]], main_variables[name_main_variables[5]]]



        medidas = []
        for index in range(len(tiempo_minutos)):
            medidas.append(index+1)



        Datos = {'Id':medidas,
                 'Tiempo_minutos': tiempo_minutos,
                 'Tiempo_segundos': tiempo_segundos,
                 'S1': resistencias[0],
                 'S2': resistencias[1],
                 'S3': resistencias[2],
                 'S4': resistencias[3],
                 name_main_variables[4]: gases[0],
                 name_main_variables[5]: gases[1],
                 name_parametros_variables[0]: caudal,
                 'Tamb': t_ambiente,
                 'Humidity': humidity,

                 }


        data = pd.DataFrame(Datos, columns=['Id','Tiempo_minutos','Tiempo_segundos',
                                            'S1', 'S2', 'S3', 'S4',
                                            name_main_variables[4], name_main_variables[5],
                                            name_parametros_variables[0], 'Tamb', 'Humidity'])

        exportar_excel(data,path_output,name_folder)

        return data,[name_main_variables[4],name_main_variables[5]]



    except:
        print("[INFO] Error en ",path)
        exit()

def exportar_excel(data,path,name):
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

    # Numero de filas y columnas del fichero
    rows = data.shape[0]
    cols = data.shape[1]

    # Abrimos el archivo excel
    writer = pd.ExcelWriter(path)
    workbook = writer.book

    # Escribimos los datos
    data.to_excel(writer, index=None,header=True,sheet_name='Datos')

    # Cerramos el libro
    workbook.close()

    return path

def procesar_caracteristicas(data,path,name):


    path = path+name+'.xlsx' # Path


    Id =data[0]
    Respuestas1 = data[1]
    Respuestas2 = data[2]
    Respuestas3 = data[3]
    Respuestas4 = data[4]

    Humidity = data[5]

    M_S1 = data[6]
    M_S2 = data[7]
    M_S3 = data[8]
    M_S4 = data[9]

    data = []
    title = ['Ciclo',
             'Respuesta_S1','Respuesta_S2','Respuesta_S3','Respuesta_S4',
             'Humedad',
             'M1_S1','M2_S1','M3_S1',
             'M1_S2','M2_S2','M3_S2',
             'M1_S3','M2_S3','M3_S3']

    data.append(title)
    for index_i in range(len(Humidity)):
        data.append([(index_i+1),
                     Respuestas1[index_i], Respuestas2[index_i], Respuestas3[index_i], Respuestas4[index_i],
                     Humidity[index_i],
                     M_S1[index_i][0],M_S1[index_i][1],M_S1[index_i][2],
                     M_S2[index_i][0],M_S2[index_i][1],M_S2[index_i][2],
                     M_S3[index_i][0],M_S3[index_i][1],M_S3[index_i][2],
                     M_S4[index_i][0],M_S4[index_i][1],M_S4[index_i][2]])

    # Creamos un woorkbook en una carpeta
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet(name='Caracteristicas')


    for row, item in enumerate(data):
        for col in range(len(data[0])):
            worksheet.write(row, col, item[col])


    workbook.close()


