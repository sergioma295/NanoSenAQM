import argparse
import os,shutil
import sys
import pandas as pd
from matplotlib.pyplot import figure, xlabel, ylabel, show, title, legend, savefig


def init():
    # Comprobación de seguridad, ejecutar sólo si se reciben 2 argumentos reales
    path ='Data/'
    parser = argparse.ArgumentParser(description='Guía de ayuda del programa')
    parser.add_argument('--f', metavar='Nombre Fichero Salida',help='Introduce el fichero a analizar: Ej: python main.py --f 07-17-2019 --t 1')
    parser.add_argument('--t', metavar='Tipo de linea',help='Introduce el tipo de fichero [1-Linea ozono 2-Linea Wiinose]')
    args = parser.parse_args()
    path  = path+args.f
    path1 = path + '/Datos Procesados/'
    path2 = path + '/excel/'
    path3 = path + '/Imgs/'
    tipo =args.t

    origen = 'Ficheros/'
    destino = path2


    try:
        os.stat(path)
        shutil.rmtree(path)
        ruta = crear_directorios(path,path1,path2,path3,origen,destino)
        print("La carpeta ya existe")
    except:
        ruta = crear_directorios(path,path1,path2,path3,origen,destino)




    print("------------------------------------------------------------------------------")
    print("--------------------------------- BIENVENIDO ---------------------------------")
    print("------------------------------------------------------------------------------")
    return ruta,path,path1,path2,path3,tipo

def crear_directorios(path,path1,path2,path3,origen,destino):
    os.mkdir(path)
    os.mkdir(path1)
    os.mkdir(path2)
    os.mkdir(path3)

    print("Directorio creado")
    if (os.path.isdir(origen)):
        try:

            files = []
            for r, d, f in os.walk(origen):
                for file in f:
                    if '.xlsx' in file:
                        files.append(os.path.join(r, file))

            for f in files:
                print(f)
        except:
            print("Error moviendo el archivo")

        ruta = shutil.move(f, destino)
        print('El directorio ha sido movido a', ruta)
    else:
        print("No existe ningun archivo en la carpeta de Ficheros")

    return ruta

def load_data_linea_wiinose(path):
    try:

        excel = pd.ExcelFile(path)
        main_variables = pd.read_excel(excel,sheet_name='resistencias')
        parametros = pd.read_excel(excel, sheet_name='parametros')



        tiempo_minutos = parametros['min']

        tiempo_segundos = []
        for index in range(len(tiempo_minutos)):
            tiempo_segundos.append(int(tiempo_minutos[index]*60))

        resistencias = [main_variables['R1'], main_variables['R2'], main_variables['R3'],main_variables['R4']]
        gases = [main_variables['NO2(ppm)']*1000, main_variables['CO (ppm)']*1000]
        caudal_total = parametros['Q (mL/min)']

        caudal_1 = []
        caudal_2 = []
        caudal_3 = []
        caudal_4 = []
        caudal_5 = []

        I1 = []
        I2 = []
        I3 = []
        I4 = []

        V1 = []
        V2 = []
        V3 = []
        V4 = []

        P1 = []
        P2 = []
        P3 = []
        P4 = []

        medidas = []
        for index in range(len(tiempo_minutos)):
            caudal_1.append('NaN Wiinose')
            caudal_2.append('NaN Wiinose')
            caudal_3.append('NaN Wiinose')
            caudal_4.append('NaN Wiinose')
            caudal_5.append('NaN Wiinose')

            V1.append('NaN Wiinose')
            V2.append('NaN Wiinose')
            V3.append('NaN Wiinose')
            V4.append('NaN Wiinose')

            I1.append('NaN Wiinose')
            I2.append('NaN Wiinose')
            I3.append('NaN Wiinose')
            I4.append('NaN Wiinose')

            P1.append('NaN Wiinose')
            P2.append('NaN Wiinose')
            P3.append('NaN Wiinose')
            P4.append('NaN Wiinose')

            medidas.append(index+1)



        Datos = {'Medidas':medidas,
                 'Tiempo_segundos': tiempo_segundos,
                 'Tiempo_minutos':tiempo_minutos,
                 'Qt':caudal_total,
                 'Q1': caudal_1,
                 'Q2': caudal_2,
                 'Q3': caudal_3,
                 'Q4': caudal_4,
                 'Q5': caudal_5,
                 'R1': resistencias[0],
                 'R2': resistencias[1],
                 'R3': resistencias[2],
                 'R4': resistencias[3],
                 'Gas1': gases[0],
                 'Gas2': gases[1],
                 'V1':V1,
                 'V2': V2,
                 'V3': V3,
                 'V4': V4,
                 'I1':I1,
                 'I2': I2,
                 'I3': I3,
                 'I4': I4,
                 'P1':P1,
                 'P2': P2,
                 'P3': P3,
                 'P4': P4
                 }


        data = pd.DataFrame(Datos, columns=['Medidas','Tiempo_segundos','Tiempo_minutos','Qt','Q1','Q2','Q3','Q4','Q5','R1', 'R2', 'R3', 'R4', 'Gas1', 'Gas2',
                                            'V1','V2','V3','V4','I1','I2','I3','I4','P1','P2','P3','P4'])



    except:
        print("Error en ",path)



    return data


def load_data_linea_ozono(path):
    try:
        excel = pd.ExcelFile(path)
        main_variables = pd.read_excel(excel,sheet_name='Main Variables')
        electrometer = pd.read_excel(excel, sheet_name='Electrometer')
        iray = pd.read_excel(excel, sheet_name='IRAY - V4CH')
        gmu6 = pd.read_excel(excel, sheet_name='GMU6')
        filtered = pd.read_excel(excel, sheet_name='Filtered Resistances  ohm ')


        tiempo_segundos = main_variables['Time [s]']
        #tiempo_minutos_ = tiempo_segundos.values/60

        tiempo_minutos = []
        for index in range(len(tiempo_segundos)):
            tiempo_minutos.append(int(tiempo_segundos[index]/60))

        resistencias = [main_variables['R1 [ohm]'], main_variables['R2 [ohm]'], main_variables['R3 [ohm]'],main_variables['R4 [ohm]']]
        gases = [main_variables['[NO2] [ppbv]'],main_variables['[O3] [ppbv]']]


        caudal_total = gmu6['Total flow [ml/min]']
        caudal_1     = gmu6['C1 Flow [ml/min]']
        caudal_2     = gmu6['C2 Flow [ml/min]']
        caudal_3     = gmu6['C3 Flow [ml/min]']
        caudal_4     = gmu6['C4 Flow [ml/min]']
        caudal_5     = gmu6['C5 Flow [ml/min]']


        V1 = iray['V Heating R1 [mV]']
        V2 = iray['V Heating R2 [mV]']
        V3 = iray['V Heating R3 [mV]']
        V4 = iray['V Heating R4 [mV]']
        I1 = iray['I Heating R1 [mA]']
        I2 = iray['I Heating R2 [mA]']
        I3 = iray['I Heating R3 [mA]']
        I4 = iray['I Heating R4 [mA]']

        medidas = []
        for index in range(len(tiempo_segundos)):
            medidas.append(index+1)

        P1 = []
        P2 = []
        P3 = []
        P4 = []

        for index in range(len(V1)):
            P1.append((V1[index]/1000) * (I1[index]/1000)*1000)
            P2.append((V2[index]/1000) * (I2[index]/1000)*1000)
            P3.append((V3[index]/1000) * (I3[index]/1000)*1000)
            P4.append((V4[index]/1000) * (I4[index]/1000)*1000)

        Datos = {'Medidas':medidas,
                 'Tiempo_segundos': tiempo_segundos,
                 'Tiempo_minutos':tiempo_minutos,
                 'Qt':caudal_total,
                 'Q1': caudal_1,
                 'Q2': caudal_2,
                 'Q3': caudal_3,
                 'Q4': caudal_4,
                 'Q5': caudal_5,
                 'R1': resistencias[0],
                 'R2': resistencias[1],
                 'R3': resistencias[2],
                 'R4': resistencias[3],
                 'Gas1': gases[0],
                 'Gas2': gases[1],
                 'V1':V1,
                 'V2': V2,
                 'V3': V3,
                 'V4': V4,
                 'I1':I1,
                 'I2': I2,
                 'I3': I3,
                 'I4': I4,
                 'P1':P1,
                 'P2': P2,
                 'P3': P3,
                 'P4': P4
                 }


        data = pd.DataFrame(Datos, columns=['Medidas','Tiempo_segundos','Tiempo_minutos','Qt','Q1','Q2','Q3','Q4','Q5','R1', 'R2', 'R3', 'R4', 'Gas1', 'Gas2',
                                            'V1','V2','V3','V4','I1','I2','I3','I4','P1','P2','P3','P4'])



    except:
        print("Error en ",path)



    return data

def calcular_respuestas(data):

    # Archivo proveniente de Linea ozono
    Gas = data['Gas1'].values
    # Archivo proveniente de Wiinose
    Gas = data['Gas1'].values



    R1=data['R1'].values
    R2=data['R2'].values
    R3=data['R3'].values
    R4=data['R4'].values

    item = []

    for index in range(len(Gas)-1):
        index+=1
        if Gas[index] != Gas[index-1]:
            longitud = len(item)
            if(len(item)%2)!=0:
                if Gas[index]!=0:
                    item.append(index)
                else:
                    item.append(index-1)

            else:
                if Gas[index]==0:
                    item.append(index)
                else:
                    item.append(index-1)


    if (len(item)%2)!=0:
        item.remove(item[len(item)-1])

    respuestas_1=[]
    respuestas_2=[]
    respuestas_3=[]
    respuestas_4=[]

    for index in range(len(item)):
        if index%2!=0:

            Ra1 = R1[item[index-1]]
            Rg1= R1[item[index]]

            Ra2 = R2[item[index-1]]
            Rg2 = R2[item[index]]

            Ra3 = R3[item[index-1]]
            Rg3 = R3[item[index]]

            Ra4 = R4[item[index-1]]
            Rg4 = R4[item[index]]


            resp1 = Rg1 / Ra1
            resp2 = Rg2 / Ra2
            resp3 = Rg3 / Ra3
            resp4 = Rg4 / Ra4

            respuestas_1.append(resp1)
            respuestas_2.append(resp2)
            respuestas_3.append(resp3)
            respuestas_4.append(resp4)

        ciclos = []
        for index in range(len(respuestas_1)):
            ciclos.append(index+1)

    Respuestas = {'Ciclo': ciclos,
                  'Resp1': respuestas_1,
                  'Resp2': respuestas_2,
                  'Resp3': respuestas_3,
                  'Resp4': respuestas_4,
                 }

    Respuestas = pd.DataFrame(Respuestas,
                        columns=['Ciclo','Resp1', 'Resp2', 'Resp3', 'Resp4'])

    for index in range(len(item)):
        item[index]=item[index]+2

    Index = {'Indices': item,

    }

    Index = pd.DataFrame(Index,
                        columns=['Indices'])

    return [respuestas_1,respuestas_2,respuestas_3,respuestas_4],Respuestas,Index

def representar_respuestas_R1_ciclo(respuestas,path):
    path=path+'Respuesta_R1.png'

    item = []
    for index in range(len(respuestas)):
        item.append(index+1)

    fig = figure()
    ax1 = fig.add_subplot(111)
    line1 = ax1.scatter(item,respuestas,color='black')
    ylabel("Rg/Ra")
    xlabel("Ciclo")
    title("R1")
    savefig(path)

def representar_respuestas_R2_ciclo(respuestas,path):
    path=path+'Respuesta_R2.png'

    item = []
    for index in range(len(respuestas)):
        item.append(index+1)

    fig = figure()
    ax1 = fig.add_subplot(111)
    line1 = ax1.scatter(item,respuestas,color='black')
    ylabel("Rg/Ra")
    xlabel("Ciclo")
    title("R2")
    savefig(path)

def representar_respuestas_R3_ciclo(respuestas,path):
    path=path+'Respuesta_R3.png'

    item = []
    for index in range(len(respuestas)):
        item.append(index+1)

    fig = figure()
    ax1 = fig.add_subplot(111)
    line1 = ax1.scatter(item,respuestas,color='black')
    ylabel("Rg/Ra")
    xlabel("Ciclo")
    title("R3")
    savefig(path)

def representar_respuestas_R4_ciclo(respuestas,path):
    path=path+'Respuesta_R4.png'

    item = []
    for index in range(len(respuestas)):
        item.append(index+1)

    fig = figure()
    ax1 = fig.add_subplot(111)
    line1 = ax1.scatter(item,respuestas,color='black')
    ylabel("Rg/Ra")
    xlabel("Ciclo")
    title("R4")
    savefig(path)


def representar_respuestas_ciclo(respuestas,path):
    representar_respuestas_R1_ciclo(respuestas[0])
    representar_respuestas_R2_ciclo(respuestas[1])
    representar_respuestas_R3_ciclo(respuestas[2])
    representar_respuestas_R4_ciclo(respuestas[3])
    #show()


def plot_R1(data,path):
    path=path+'R1.png'

    t = data['Tiempo_minutos'].values
    R1 = data['R1'].values
    Gas1=data['Gas1'].values
    Gas2=data['Gas2'].values


    fig1 = figure()

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(111)
    line1 = ax1.plot(t,R1,color='black')
    ylabel("Concentracion [ppbv]")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    line2 = ax2.plot(t,Gas1,'--g')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ylabel("Resistencia [Ohmios] ")
    xlabel("Tiempo [s]")
    title("R1")
    savefig(path)

def plot_R2(data,path):
    path=path+'R2.png'

    t = data['Tiempo_minutos'].values
    R2 = data['R2'].values
    Gas1=data['Gas1'].values
    Gas2=data['Gas2'].values


    fig1 = figure()

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(111)
    line1 = ax1.plot(t,R2,color='black')
    ylabel("Concentracion [ppbv]")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    line2 = ax2.plot(t,Gas1,'--g')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ylabel("Resistencia [Ohmios] ")
    xlabel("Tiempo [s]")
    title("R2")

    savefig(path)

def plot_R3(data,path):
    path=path+'R3.png'

    t = data['Tiempo_minutos'].values

    R3 = data['R3'].values
    Gas1=data['Gas1'].values
    Gas2=data['Gas2'].values


    fig1 = figure()

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(111)
    line1 = ax1.plot(t,R3,color='black')
    ylabel("Concentracion [ppbv]")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    line2 = ax2.plot(t,Gas1,'--g')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ylabel("Resistencia [Ohmios] ")
    xlabel("Tiempo [s]")
    title("R3")
    savefig(path)

def plot_R4(data,path):
    path=path+'R4.png'

    t = data['Tiempo_minutos'].values
    R4 = data['R4'].values
    Gas1=data['Gas1'].values
    Gas2=data['Gas2'].values


    fig1 = figure()

    # and the first axes using subplot populated with data
    ax1 = fig1.add_subplot(111)
    line1 = ax1.plot(t,R4,color='black')
    ylabel("Concentracion [ppbv]")

    # now, the second axes that shares the x-axis with the ax1
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    line2 = ax2.plot(t,Gas1,'--g')
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    ylabel("Resistencia [Ohmios] ")
    xlabel("Tiempo [s]")
    title("R4")
    savefig(path)

def plot_all(data,respuestas,path,tipo_excel):
    plot_R1(data,path)
    plot_R2(data,path)
    plot_R3(data,path)
    plot_R4(data,path)
    representar_respuestas_R1_ciclo(respuestas[0],path)
    representar_respuestas_R2_ciclo(respuestas[1],path)
    representar_respuestas_R3_ciclo(respuestas[2],path)
    representar_respuestas_R4_ciclo(respuestas[3],path)
    #show()


def export_excel(data,Respuestas,Index,path):

    path = path + '/Datos Procesados/Sensor.xlsx'

    # Obtenemos la extension de la tabla de respuestas
    rows_respuestas = Respuestas.shape[0]
    cols_respuestas = Respuestas.shape[1]

    rows_data = data.shape[0]
    cols_data = data.shape[1]

    # Abrimos el archivo excel
    writer = pd.ExcelWriter(path)
    workbook = writer.book

    # Escribimos los datos
    data.to_excel(writer, index=None,header=True,sheet_name='Datos Medida')
    Respuestas.to_excel(writer, index=None,header=True,sheet_name='Respuestas')
    Index.to_excel(writer, index=None,header=True,sheet_name='Indices')

    # Añadimos la gráfica del comportamiento del sensor 1
    chartsheet_sensor_1= workbook.add_chartsheet()
    chart_sensor_1 = workbook.add_chart({'type': 'line'})
    chart_sensor_1.add_series({
                                'name': ['Datos Medida', 0, 9],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 13, rows_data, 13],
                                'y2_axis':1,
                                'line': {'color': 'green', 'width': 1.0, 'dash_type': 'dash'},


                              })
    chart_sensor_1.add_series({
                                'name': ['Datos Medida', 0, 13],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 9, rows_data, 9],
                                'line': {'color': 'black', 'width': 1.25},

    })

    # Titulo de gráfica
    chart_sensor_1.set_title({'name': 'S1'})

    # Título de Eje Y
    chart_sensor_1.set_y_axis({'name': 'Resistencia (Ohmios)',
                               'num_format': '0.00E+00',
                               'major_gridlines': {'visible': False},
                               })

    chart_sensor_1.set_y2_axis({'name': 'NO2 [ppb]',
                                'num_format': '0.00',
                                'major_gridlines': {'visible': False},
                                })

    # Título de Eje X
    chart_sensor_1.set_x_axis({'name': 'Tiempo (minutos)',
                               'num_format': '0'})


    # Estile del gráfico
    chart_sensor_1.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_sensor_1.set_chart(chart_sensor_1)
    chartsheet_sensor_1.name = 'Sensor 1'
    # Activamos la hoja
    chartsheet_sensor_1.activate();


    # Añadimos la gráfica del comportamiento del sensor 2
    chartsheet_sensor_2= workbook.add_chartsheet()
    chart_sensor_2 = workbook.add_chart({'type': 'line'})
    chart_sensor_2.add_series({
                                'name': ['Datos Medida', 0, 9],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 13, rows_data, 13],
                                'y2_axis': 1,
                                'line': {'color': 'green', 'width': 1.0, 'dash_type': 'dash'},

    })

    chart_sensor_2.add_series({
                                'name': ['Datos Medida', 0, 13],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 10, rows_data, 10],
                                'line': {'color': 'black', 'width': 1.25},

    })
    # Titulo de gráfica
    chart_sensor_2.set_title({'name': 'S2'})
    # Título de Eje Y
    chart_sensor_2.set_y_axis({'name': 'Resistencia (Ohmios)',
                               'num_format': '0.00E+00',
                               'major_gridlines': {'visible': False},
                               })

    chart_sensor_2.set_y2_axis({'name': 'NO2 [ppb]',
                                'num_format': '0.00',
                                'major_gridlines': {'visible': False},
                                })

    # Título de Eje X
    chart_sensor_2.set_x_axis({'name': 'Tiempo (minutos)',
                               'num_format': '0'})

    # Estile del gráfico
    chart_sensor_2.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_sensor_2.set_chart(chart_sensor_2)
    chartsheet_sensor_2.name = 'Sensor 2'
    # Activamos la hoja
    chartsheet_sensor_2.activate();

    # Añadimos la gráfica del comportamiento del sensor 3
    chartsheet_sensor_3 = workbook.add_chartsheet()
    chart_sensor_3 = workbook.add_chart({'type': 'line'})
    chart_sensor_3.add_series({
                                'name': ['Datos Medida', 0, 9],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 13, rows_data, 13],
                                'y2_axis': 1,
                                'line': {'color': 'green', 'width': 1.0, 'dash_type': 'dash'},
    })

    chart_sensor_3.add_series({
                                'name': ['Datos Medida', 0, 13],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 11, rows_data, 11],
                                'line': {'color': 'black', 'width': 1.25},
    })
    # Titulo de gráfica
    chart_sensor_3.set_title({'name': 'S3'})
    # Título de Eje Y
    chart_sensor_3.set_y_axis({'name': 'Resistencia (Ohmios)',
                               'num_format': '0.00E+00',
                               'major_gridlines': {'visible': False},
                               })

    chart_sensor_3.set_y2_axis({'name': 'NO2 [ppb]',
                                'num_format': '0.00',
                                'major_gridlines': {'visible': False},
                                })

    # Título de Eje X
    chart_sensor_3.set_x_axis({'name': 'Tiempo (minutos)',
                               'num_format': '0'})

    # Estile del gráfico
    chart_sensor_3.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_sensor_3.set_chart(chart_sensor_3)
    chartsheet_sensor_3.name = 'Sensor 3'
    # Activamos la hoja
    chartsheet_sensor_3.activate();

    # Añadimos la gráfica del comportamiento del sensor 4
    chartsheet_sensor_4 = workbook.add_chartsheet()
    chart_sensor_4 = workbook.add_chart({'type': 'line'})
    chart_sensor_4.add_series({
                                'name': ['Datos Medida', 0, 9],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 13, rows_data, 13],
                                'y2_axis': 1,
                                'line': {'color': 'green', 'width': 1.0, 'dash_type': 'dash'},
    })

    chart_sensor_4.add_series({
                                'name': ['Datos Medida', 0, 13],
                                'categories': ['Datos Medida', 1, 2, rows_data, 2],
                                'values': ['Datos Medida', 1, 12, rows_data, 12],
                                'line': {'color': 'black', 'width': 1.25},
    })

    # Titulo de gráfica
    chart_sensor_4.set_title({'name': 'S4'})
    # Título de Eje Y
    chart_sensor_4.set_y_axis({'name': 'Resistencia (Ohmios)',
                               'num_format': '0.00E+00',
                               'major_gridlines': {'visible': False},
                               })

    chart_sensor_4.set_y2_axis({'name': 'NO2 [ppb]',
                                'num_format': '0.00',
                                'major_gridlines': {'visible': False},
                                })

    # Título de Eje X
    chart_sensor_4.set_x_axis({'name': 'Tiempo (minutos)',
                               'num_format': '0'})
    # Estile del gráfico
    chart_sensor_4.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_sensor_4.set_chart(chart_sensor_4)
    chartsheet_sensor_4.name = 'Sensor 4'
    # Activamos la hoja
    chartsheet_sensor_4.activate();

    # Añadimos la gráfica de Respuestas del sensor 1
    chartsheet_respuesta_1 = workbook.add_chartsheet()
    chart_respuesta_1 = workbook.add_chart({'type': 'scatter'})
    chart_respuesta_1.add_series({
                        'name': ['Respuestas', 0, 1],
                        'categories': ['Respuestas', 1, 0, rows_respuestas, 0],
                        'values': ['Respuestas', 1, 1, rows_respuestas, 1],
                        'marker': {
                                    'type': 'triangle',
                                    'size': 8,
                                    'border': {'color': 'black'},
                                    'fill': {'color': 'black'}}
    })

    # Titulo de gráfica
    chart_respuesta_1.set_title({'name': 'Respuesta S1'})
    # Título de Eje Y
    chart_respuesta_1.set_y_axis({'name': 'Rg2/Ra2',
                               'major_gridlines': {'visible': False},
                               })

    # Título de Eje X
    chart_respuesta_1.set_x_axis({'name': 'Ciclos'})
    # Estile del gráfico
    chart_respuesta_1.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_respuesta_1.set_chart(chart_respuesta_1)
    chartsheet_respuesta_1.name='Respuesta_S1'
    # Activamos la hoja
    chartsheet_respuesta_1.activate();


    # Añadimos la gráfica de Respuestas del sensor 2
    chartsheet_respuesta_2 = workbook.add_chartsheet()
    chart_respuesta_2 = workbook.add_chart({'type': 'scatter'})
    chart_respuesta_2.add_series({
                        'name': ['Respuestas', 0, 2],
                        'categories': ['Respuestas', 1, 0, rows_respuestas, 0],
                        'values': ['Respuestas', 1, 2, rows_respuestas, 2],
                        'marker': {
                            'type': 'triangle',
                            'size': 8,
                            'border': {'color': 'black'},
                            'fill': {'color': 'black'}}
    })

    # Titulo de gráfica
    chart_respuesta_2.set_title({'name': 'Respuesta S2'})
    # Título de Eje X
    chart_respuesta_2.set_x_axis({'name': 'Ciclos'})
    # Título de Eje Y
    chart_respuesta_2.set_y_axis({'name': 'Rg2/Ra2',
                                  'major_gridlines': {'visible': False},
                                  })
    # Estile del gráfico
    chart_respuesta_2.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_respuesta_2.set_chart(chart_respuesta_2)
    chartsheet_respuesta_2.name='Respuesta_S2'
    # Activamos la hoja
    chartsheet_respuesta_2.activate();

    # Añadimos la gráfica de Respuestas del sensor 3
    chartsheet_respuesta_3 = workbook.add_chartsheet()
    chart_respuesta_3 = workbook.add_chart({'type': 'scatter'})
    chart_respuesta_3.add_series({
                        'name': ['Respuestas', 0, 3],
                        'categories': ['Respuestas', 1, 0, rows_respuestas, 0],
                        'values': ['Respuestas', 1, 3, rows_respuestas, 3],
                        'marker': {
                            'type': 'triangle',
                            'size': 8,
                            'border': {'color': 'black'},
                            'fill': {'color': 'black'}}
    })

    # Titulo de gráfica
    chart_respuesta_3.set_title({'name': 'Respuesta S3'})
    # Título de Eje X
    chart_respuesta_3.set_x_axis({'name': 'Ciclos'})
    # Título de Eje Y
    chart_respuesta_3.set_y_axis({'name': 'Rg3/Ra3',
                                  'major_gridlines': {'visible': False},
                                  })
    # Estile del gráfico
    chart_respuesta_3.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_respuesta_3.set_chart(chart_respuesta_3)
    chartsheet_respuesta_3.name='Respuesta_S3'
    # Activamos la hoja
    chartsheet_respuesta_3.activate();


    # Añadimos la gráfica de Respuestas del sensor 4
    chartsheet_respuesta_4 = workbook.add_chartsheet()
    chart_respuesta_4 = workbook.add_chart({'type': 'scatter'})
    chart_respuesta_4.add_series({
                        'name': ['Respuestas', 0, 4],
                        'categories': ['Respuestas', 1, 0, rows_respuestas, 0],
                        'values': ['Respuestas', 1, 4, rows_respuestas, 4],
                        'marker': {
                            'type': 'triangle',
                            'size': 8,
                            'border': {'color': 'black'},
                            'fill': {'color': 'black'}}
    })

    # Titulo de gráfica
    chart_respuesta_4.set_title({'name': 'Respuesta S4'})
    # Título de Eje X
    chart_respuesta_4.set_x_axis({'name': 'Ciclos'})
    # Título de Eje Y
    chart_respuesta_4.set_y_axis({'name': 'Rg4/Ra4',
                                  'major_gridlines': {'visible': False},
                                  })
    # Estile del gráfico
    chart_respuesta_4.set_style(11)
    # Añadimos el gráfico a la hoja de excel
    chartsheet_respuesta_4.set_chart(chart_respuesta_4)
    chartsheet_respuesta_4.name='Respuesta_S4'
    # Activamos la hoja
    chartsheet_respuesta_4.activate();





    # Cerramos el libro
    workbook.close()
