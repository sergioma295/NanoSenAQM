import argparse
import math
import os,shutil
import sys
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
import seaborn as sns
import numpy as np
def get_sample_time(Data):
    t_m = Data['Tiempo_minutos']
    t_s = Data['Tiempo_segundos']

    # Obtención del sample time y almacenamiento en una lista
    sample_time = []
    for index in range(len(t_s)-1):
        s_t = t_s[index+1] - t_s[index]
        sample_time.append(s_t)

    # Comprobamos que el sample time tiene la misma longitud -1 que la serie temporal
    if(len(sample_time)==len(t_s)-1):
        pass
    else:
        print("[INFO] Error. Sample Time mal dimensionado")

    # Obtenemos el valor medio del sample time
    sample_time_mean = get_statistics(sample_time,'Sample Time',0)

    return sample_time,sample_time_mean

def get_statistics(variable,name, output):
    # Convertimos de List a DataFrame
    data_frame = pd.DataFrame(variable)

    # Medidas de tendencia central
    media = data_frame.mean().values[0]                     # Media aritmética
    media_geometrica = stats.gmean(data_frame)[0]           # Media geométrica
    media_armonica  = stats.hmean(data_frame)[0]             # Media armónica
    mediana = data_frame.median().values[0]                 # Mediana
    moda = data_frame.mode().values[0][0]                   # Moda

    # Medidas de dispersión
    varianza = data_frame.var().values[0]                    # Varianza
    varianza_estandar = data_frame.std().values[0]           # Varianza estańdar

    # Resumen estadístico
    descripcion_estadistica = data_frame.describe()

    if (output ==0):
        return media
    elif( output == 1):
        return media_geometrica

    elif (output == 3):
        return media_armonica

    elif (output == 4):
        return mediana

    elif (output == 5):
        return moda

    elif (output == 6):
        return varianza

    elif (output == 7):
        return varianza_estandar

    elif (output == 8):
        return descripcion_estadistica
    else:
        print("[INFO] Error. Devolución estadística")




def get_gas_cycles(Sensor, Gas, Index):
    # Variable para almacenar los índices de cada ciclo
    samples = []

    # Variables temporales para almacenar el valor de la resistencia de los sensores.
    s1 = Sensor[0]
    s2 = Sensor[1]
    s3 = Sensor[2]
    s4 = Sensor[3]

    # Variables de salida del método
    data_s1 = []
    data_s2 = []
    data_s3 = []
    data_s4 = []
    data_gas = []

    # Recorremos la lista con los índices que indican un cambio de concenctración
    for index in range(len(Index)):
        # Comprobamos si el índice es impar o su valor es mayor a la longitud del número de cambios de concentración
        # menos tres. En caso contrario, añadimos al vector las resistencias desde dicho índice a dicho índice + 3.
        if index % 2 != 0 or index > (len(Index) - 3):
            pass
        else:
            # Cálculo de índices para el límite inferior y el superior.
            lim_inf = Index[index]
            lim_sup = Index[index + 3]

            # Obtención de la concentración del gas
            gas = Gas[lim_inf:lim_sup]

            # Variable que almacena los índices de cada ciclo
            samples.append(Index[index:(index + 4)])

            # Obtención de los valores que se encuentran entre los límites para cada sensor.
            # SENSOR 1
            s1_ = s1[lim_inf:lim_sup]

            # SENSOR 2
            s2_ = s2[lim_inf:lim_sup]

            # SENSOR 3
            s3_ = s3[lim_inf:lim_sup]

            # SENSOR 4
            s4_ = s4[lim_inf:lim_sup]

            data_s1.append(s1_)
            data_s2.append(s2_)
            data_s3.append(s3_)
            data_s4.append(s4_)
            data_gas.append(gas)

    return data_s1, data_s2, data_s3, data_s4, data_gas, samples






def get_samples_cycles(Sensor, Gas1, Gas2, Index1, Index2):

    # Se convierten las variables NO2 y CO a List.
    gas1 = Gas1.tolist()
    gas2 = Gas2.tolist()


    # Variables para almacenar los datos de los gases
    GAS1 = 0
    GAS2 = 0

    # Un ciclo contiene todos los puntos desde el Pt.A - Pt.D

    #                                       ----------------
    #                                       |              |
    #                                       |              |
    #                           ------------|              |----------
    #                           Pt.A        Pt.B          Pt.C       Pt.D


    # Si la longitud de la variable no2_index o co_index > 2, existen ciclos. En cc NO existen ciclos y dicha variable
    # solo tendrá dos posiciones ocupadas, el valor inicial y final de dicho experimento.
    if (len(Index1) != 2):

        S1_GAS1,S2_GAS1,S3_GAS1,S4_GAS1,GAS1,GAS1_samples = get_gas_cycles(Sensor = Sensor, Gas = gas1, Index = Index1)

    if(len(Index2)!= 2):
        S1_GAS2,S2_GAS2,S3_GAS2,S4_GAS2,GAS2,GAS2_samples = get_gas_cycles(Sensor = Sensor, Gas = gas2, Index=Index2)


    if(GAS1)!=0 and GAS2 !=0:
        # Agrupación de datos del sensor y los gases
        data_s1 = [S1_GAS1, GAS1, S1_GAS2, GAS2]
        data_s2 = [S2_GAS1, GAS1, S2_GAS2, GAS2]
        data_s3 = [S3_GAS1, GAS1, S3_GAS2, GAS2]
        data_s4 = [S4_GAS1, GAS1, S4_GAS2, GAS2]

    elif(GAS1!=0):
        # Agrupación de datos del sensor y los gases
        # Copiamos e inicializamos a 0 la salida mantenga siempre la misma estructura
        GAS2 = [[0 for i in range(len(GAS1[0]))] for j in range(len(GAS1))]

        S1_GAS2 = [[0 for i in range(len(S1_GAS1[0]))] for j in range(len(S1_GAS1))]
        S2_GAS2 = [[0 for i in range(len(S2_GAS1[0]))] for j in range(len(S2_GAS1))]
        S3_GAS2 = [[0 for i in range(len(S3_GAS1[0]))] for j in range(len(S3_GAS1))]
        S4_GAS2 = [[0 for i in range(len(S4_GAS1[0]))] for j in range(len(S4_GAS1))]

        data_s1 = [S1_GAS1, GAS1,S1_GAS2, GAS2]
        data_s2 = [S2_GAS1, GAS1,S2_GAS2, GAS2]
        data_s3 = [S3_GAS1, GAS1,S3_GAS2, GAS2]
        data_s4 = [S4_GAS1, GAS1,S4_GAS2, GAS2]

        # Copiamos e inicializamos a 0 el valor del GAS2_samples para que la salida mantenga siempre la misma estructura
        GAS2_samples = [[0 for i in range(len(GAS1_samples))] for j in range(len(GAS1_samples))]


    elif (GAS2 != 0):
        # Agrupación de datos del sensor y los gases
        # Copiamos e inicializamos a 0 la salida mantenga siempre la misma estructura
        GAS1 = [[0 for i in range(len(GAS2[0]))] for j in range(len(GAS2))]

        S1_GAS1 = [[0 for i in range(len(S1_GAS2[0]))] for j in range(len(S1_GAS2))]
        S2_GAS1 = [[0 for i in range(len(S2_GAS2[0]))] for j in range(len(S2_GAS2))]
        S3_GAS1 = [[0 for i in range(len(S3_GAS2[0]))] for j in range(len(S3_GAS2))]
        S4_GAS1 = [[0 for i in range(len(S4_GAS2[0]))] for j in range(len(S4_GAS2))]

        data_s1 = [S1_GAS1, GAS1, S1_GAS2, GAS2]
        data_s2 = [S2_GAS1, GAS1, S2_GAS2, GAS2]
        data_s3 = [S3_GAS1, GAS1, S3_GAS2, GAS2]
        data_s4 = [S4_GAS1, GAS1, S4_GAS2, GAS2]

        # Copiamos e inicializamos a 0 el valor del GAS1_samples para que la salida mantenga siempre la misma estructura
        GAS1_samples = [[0 for i in range(len(GAS2_samples))] for j in range(len(GAS2_samples))]

    samples = GAS1_samples, GAS2_samples

    return data_s1, data_s2, data_s3, data_s4, samples


def calculate_slope(r2,r1, t2,t1):

    incResistencia = r2 - r1
    incTiempo = t2 - t1

    m = (incResistencia) / incTiempo
    n = r2 - m*t2

    return m,n


def plot_slope_tramo(Time, Sensor,Gas, Time_Final, Time_Initial,Sample_Time, Slope, N,Path, Title, Id):
    time = Time.tolist()
    a = len(Sensor)
    b = len(time)
    # Obtenemos los valores límite de cada tramo calculados anteriormente
    # TRAMO 1
    tf1 = Time_Final[0]
    ti1 = Time_Initial[0]

    # TRAMO 2
    tf2 = Time_Final[1]
    ti2 = Time_Initial[1]

    # TRAMO 3
    tf3 = Time_Final[2]
    ti3 = Time_Initial[2]

    # Obtenemos las pendientes de los tres tramos
    # Tramo 1
    m1 = Slope[0]
    n1 = N[0]
    # Calculamos la recta para representarla
    x1 = np.linspace(int(ti1),int(tf1),int(Sample_Time))
    y1 = m1*x1 + n1

    # Tramo 2
    m2 = Slope[1]
    n2 = N[1]
    # Calculamos la recta para representarla
    x2 = np.linspace(int(ti2),int(tf2),int(Sample_Time))
    y2 = m2*x2 + n2

    # Tramo 3
    m3 = Slope[2]
    n3 = N[2]
    # Calculamos la recta para representarla
    x3 = np.linspace(int(ti3),int(tf3),int(Sample_Time))
    y3 = m3*x3 + n3

    fig, ax1 = plt.subplots()
    fig.suptitle(Title, fontsize=16)

    color = 'tab:blue'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Resistance (Ohms)', color=color)
    ax1.plot(time, Sensor, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax1.plot(x1, y1, '--r', label='slope1')
    ax1.plot(x2, y2, '--m', label='slope2')
    ax1.plot(x3, y3, '--y', label='slope3')


    plt.legend(loc='upper right')
    plt.grid()

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel(Id, color=color)  # we already handled the x-label with ax1
    ax2.plot(time, Gas, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(Path)
    plt.close(fig)


def procesar_pendientes(sensor,index,t1_1,t2_1,t1_2,t2_2,t1_3,t2_3,tramo1_inf_R, tramo1_sup_R,tramo2_inf_R, tramo2_sup_R,tramo3_inf_R, tramo3_sup_R):
    r1_1_1 = sensor[index][tramo1_inf_R]  # Punto del sensor S1, 1 en tramo 1
    r1_2_1 = sensor[index][tramo1_sup_R]  # Punto del sensor S1, 2 en tramo 1

    r1_1_2 = sensor[index][tramo2_inf_R]  # Punto del sensor S1, 1 en tramo 2
    r1_2_2 = sensor[index][tramo2_sup_R]  # Punto del sensor S1, 2 en tramo 2

    r1_1_3 = sensor[index][tramo3_inf_R]  # Punto del sensor S1, 1 en tramo 3
    r1_2_3 = sensor[index][tramo3_sup_R]  # Punto del sensor S1, 2 en tramo 3

    # Calculo de pendiente (incrementoResistencia / incrementoTiempo) en cada tramo
    # TRAMO 1
    m1, n1 = calculate_slope(r1_2_1, r1_1_1, t2_1, t1_1)

    # TRAMO 2
    m2, n2 = calculate_slope(r1_2_2, r1_1_2, t2_2, t1_2)

    # TRAMO 3
    m3, n3 = calculate_slope(r1_2_3, r1_1_3, t2_3, t1_3)

    slope_ = [m1, m2, m3]
    n_     = [n1, n2, n3]

    return slope_, n_


def get_slopes(Time, Sensor, Gas, Samples,Sample_Time,Path,Gas_Id):

    # Datos de los sensores
    s1 = Sensor[0]
    s2 = Sensor[1]
    s3 = Sensor[2]
    s4 = Sensor[3]

    # Datos de los gases
    gas = Gas.tolist()

    # Variable para almacenar las pendientes
    slope1 = [] # Variable para almacenar pendientes del sensor 1
    slope2 = [] # Variable para almacenar pendientes del sensor 2
    slope3 = [] # Variable para almacenar pendientes del sensor 3
    slope4 = [] # Variable para almacenar pendientes del sensor 4

    for index in range(len(Samples)):
        # Obtenemos los índices de resitencia que se encuentran dentro del ciclo, es decir, en presencia de un gas
        # contaminante.
        # Estos límites se calculan para ser utilizados en el array de resistencia
        lim_inf_G = Samples[index][1]
        lim_sup_G = Samples[index][2]

        # Estos límites se calculan para ser utilizados en el array de tiempos y concentración de gas
        lim_inf_R = Samples[index][1] - Samples[index][0]
        lim_sup_R = Samples[index][2] - Samples[index][1] + lim_inf_R

        # Obtenemos el ancho de ciclo (numero de puntos). Dividimos en tres el total de puntos para obtener tres tramos
        num_samples = (lim_sup_R - lim_inf_R)/3


        # Obtenemos índices tramos
        # TRAMO 1
        # Resistencia
        tramo1_inf_R = int(lim_inf_R)
        tramo1_sup_R = int(tramo1_inf_R + num_samples)

        # Tiempo y Concentración
        tramo1_inf_G = int(lim_inf_G)
        tramo1_sup_G = int(tramo1_inf_G + num_samples)

        # TRAMO 2
        tramo2_inf_R = int(tramo1_sup_R)
        tramo2_sup_R = int(tramo2_inf_R + num_samples)

        # Tiempo y Concentración
        tramo2_inf_G = int(tramo1_sup_G)
        tramo2_sup_G = int(tramo2_inf_G + num_samples)

        # TRAMO 3
        tramo3_inf_R = int(tramo2_sup_R)
        tramo3_sup_R = int(tramo3_inf_R + num_samples)

        # Tiempo y Concentración
        tramo3_inf_G = int(tramo2_sup_G)
        tramo3_sup_G = int(tramo3_inf_G + num_samples)

        # Obtención del valor de tiempo en cada tramo
        # TRAMO 1
        t1_1 = Time[tramo1_inf_G]  # T1 en tramo 1
        t2_1 = Time[tramo1_sup_G]  # T2 en tramo 1

        # TRAMO 2
        t1_2 = Time[tramo2_inf_G]  # T1 en tramo 2
        t2_2 = Time[tramo2_sup_G]  # T2 en tramo 2

        # TRAMO 3
        t1_3 = Time[tramo3_inf_G]  # T1 en tramo 3
        t2_3 = Time[tramo3_sup_G]  # T2 en tramo 3

        # Plot tramo. Límite inferior del periodo completo
        a = Samples[index][0]
        b = Samples[index][3]

        # Obtención del valor de la resistencia en cada tramo. Se incluye en la función el cálculo de la pendiente y
        # su representación con el objetivo de hacer el programa modular. A continuación repetimos la llamada a la
        # función "procesar_pendientes" por cada sensor que tenemos.

        # SENSOR 1
        slope_, n_ = procesar_pendientes(s1,index,
                                     t1_1,t2_1,
                                     t1_2,t2_2,
                                     t1_3,t2_3,
                                     tramo1_inf_R, tramo1_sup_R,
                                     tramo2_inf_R, tramo2_sup_R,
                                     tramo3_inf_R, tramo3_sup_R)


        slope1.append(slope_)

        # Ponemos un título a la figura y al fichero para guardarla
        title = 'Slope_S1_Cycle_'+str(index+1)+'_'+Gas_Id
        path = Path+'Slopes/S1/'+title+'.png'
        plot_slope_tramo(Time = Time[a:b],Sensor = s1[index],Gas = gas[a:b],Time_Final = [t2_1,t2_2,t2_3],Time_Initial = [t1_1,t1_2,t1_3],Sample_Time = Sample_Time,Slope = slope_,N = n_,Path = path,Title = title, Id = Gas_Id)

        # SENSOR 2
        slope_,n_ = procesar_pendientes(s2,index,
                                     t1_1,t2_1,
                                     t1_2,t2_2,
                                     t1_3,t2_3,
                                     tramo1_inf_R, tramo1_sup_R,
                                     tramo2_inf_R, tramo2_sup_R,
                                     tramo3_inf_R, tramo3_sup_R)


        slope2.append(slope_)

        title = 'Slope_S2_Cycle_'+ str(index+1)+'_'+Gas_Id
        path = Path+'Slopes/S2/'+title+'.png'
        plot_slope_tramo(Time = Time[a:b],Sensor = s2[index],Gas = gas[a:b],Time_Final = [t2_1,t2_2,t2_3], Time_Initial = [t1_1,t1_2,t1_3], Sample_Time = Sample_Time,Slope = slope_,N = n_,Path = path,Title = title, Id = Gas_Id)

        # SENSOR 3
        slope_,n_ = procesar_pendientes(s3,index,
                                     t1_1,t2_1,
                                     t1_2,t2_2,
                                     t1_3,t2_3,
                                     tramo1_inf_R, tramo1_sup_R,
                                     tramo2_inf_R, tramo2_sup_R,
                                     tramo3_inf_R, tramo3_sup_R)


        slope3.append(slope_)

        title = 'Slope_S3_Cycle_'+ str(index+1)+'_'+Gas_Id
        path = Path+'Slopes/S3/'+title+'.png'
        plot_slope_tramo(Time = Time[a:b],Sensor = s3[index],Gas = gas[a:b],Time_Final = [t2_1,t2_2,t2_3], Time_Initial = [t1_1,t1_2,t1_3], Sample_Time = Sample_Time,Slope = slope_,N = n_,Path = path, Title = title, Id = Gas_Id)

        # SENSOR 4
        slope_,n_ = procesar_pendientes(s4,index,
                                     t1_1,t2_1,
                                     t1_2,t2_2,
                                     t1_3,t2_3,
                                     tramo1_inf_R, tramo1_sup_R,
                                     tramo2_inf_R, tramo2_sup_R,
                                     tramo3_inf_R, tramo3_sup_R)


        slope4.append(slope_)

        title = 'Slope_S4_Cycle_' + str(index+1)+'_'+Gas_Id
        path = Path+'Slopes/S4/'+title+'.png'
        plot_slope_tramo(Time = Time[a:b],Sensor = s4[index],Gas = gas[a:b],Time_Final = [t2_1,t2_2,t2_3],Time_Initial = [t1_1,t1_2,t1_3], Sample_Time = Sample_Time,Slope = slope_,N = n_,Path = path, Title = title, Id = Gas_Id)

    return [slope1,slope2,slope3,slope4]

def get_responses_with_humidity(Sensor, Samples, Humidity):
    s1 = Sensor[0]
    s2 = Sensor[1]
    s3 = Sensor[2]
    s4 = Sensor[3]

    # Inicilización de las variables donde se van añadir las respuestas.
    rs1 = []
    rs2 = []
    rs3 = []
    rs4 = []
    hum = []

    for index in range(len(Samples)):
        # Obtenemos los índices de la resistencia para obtener la respuesta. Los índices son calculados como:
        # Para el Rair, se resta el valor del segundo elemento con el primero
        # Para el Rgas, se resta el valor del tercer elemento con el segundo y se suma el Rair
        Rair_index = Samples[index][1] - Samples[index][0]
        Rgas_index = Samples[index][2] - Samples[index][1] + Rair_index

        # Obtención Respuestas S1
        Rair = s1[index][Rair_index]
        Rgas = s1[index][Rgas_index]
        Rs1 = Rgas/Rair
        rs1.append(Rs1)


        # Obtención Respuestas S2
        Rair = s2[index][Rair_index]
        Rgas = s2[index][Rgas_index]

        Rs2 = Rgas/Rair
        rs2.append(Rs2)

        # Obtención Respuestas S3
        Rair = s3[index][Rair_index]
        Rgas = s3[index][Rgas_index]

        Rs3 = Rgas/Rair
        rs3.append(Rs3)

        # Obtención Respuestas S4
        Rair = s4[index][Rair_index]
        Rgas = s4[index][Rgas_index]

        Rs4 = Rgas/Rair
        rs4.append(Rs4)

        # Calculamos la humedad media en presencia del gas.
        lim_hum_sup = int(Samples[index][2])
        lim_hum_inf = int(Samples[index][1])
        temp_hum = Humidity[lim_hum_inf:lim_hum_sup]

        hum_mean = get_statistics(temp_hum, 'Humidity',0)
        hum.append(hum_mean)

    return rs1, rs2, rs3, rs4, hum


def get_gases(gas1, gas2):
    # Creamos dos tipos de variables para almacenar los índices y el número de ciclos de cada gas
    num_cycle_gas1 = 0
    num_cycle_gas2 = 0
    gas1_index = [0]
    gas2_index = [0]
    for index in range(len(gas1) - 1):
        if (gas1[index + 1] == gas1[index] or np.math.isnan(gas1[index+1])):
            pass
        else:
            gas1_index.append(index)

            num_cycle_gas1 += 1

        if (gas2[index + 1] == gas2[index] or np.math.isnan(gas2[index+1])):
            pass
        else:
            gas2_index.append(index)
            num_cycle_gas2 += 1

    # Añadimos el último tramo.
    gas1_index.append(len(gas1)-1)
    gas2_index.append(len(gas2)-1)

    # Número de ciclos de la medida.
    num_cycle_gas1 /= 2
    num_cycle_gas2 /= 2

    return num_cycle_gas1, num_cycle_gas2, gas1_index, gas2_index


def get_characteristics(Data, Gases,Sample_Time, Path):

    # Guardamos cada parámetro en una variable
    t_s = Data['Tiempo_segundos']
    gas1 = Data[Gases[0]]
    gas2  = Data[Gases[1]]
    gas1_name = Gases[0]        # Nombre Gas 1
    gas2_name = Gases[1]        # Nombre Gas 2
    s1 = Data['S1'].tolist()
    s2 = Data['S2'].tolist()
    s3 = Data['S3'].tolist()
    s4 = Data['S4'].tolist()
    humidity = Data['Humidity'].tolist()

    # Obtenemos dichos índices y número de cicos.
    num_cycle_gas1, num_cycle_gas2, gas1_index, gas2_index = get_gases(gas1, gas2)

    # Obtenemos los puntos correspondientes a cada ciclo.
    data_s1, data_s2, data_s3, data_s4, samples = get_samples_cycles(Sensor = [s1,s2,s3,s4], Gas1 = gas1, Gas2 = gas2, Index1 = gas1_index, Index2 = gas2_index)

    # Obtenemos las respuestas correspondientes a cada ciclo para el gas determinado
    # En primer lugar se comprueba con cuantos gases se han trabajado.
    if(num_cycle_gas1>0 and num_cycle_gas2>0):
        print("\n------------------------------------------------------------------------------\n")
        print("Procesando datos. Porfavor, espere...")
        print("\n------------------------------------------------------------------------------\n")


        Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles = get_responses_with_humidity(Sensor = [data_s1[0],data_s2[0],data_s3[0],data_s4[0]],Samples = samples[0], Humidity = humidity)
        Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles = get_responses_with_humidity(Sensor = [data_s1[2],data_s2[2],data_s3[2],data_s4[2]], Samples=samples[1], Humidity = humidity)

        # Obtenemos las pendientes de cada ciclo
        Gas1_slopes = get_slopes(Time = t_s, Sensor = [data_s1[0],data_s2[0],data_s3[0],data_s4[0]], Gas = gas1, Samples = samples[0], Sample_Time = Sample_Time, Path = Path, Gas_Id = gas1_name)
        Gas2_slopes = get_slopes(Time = t_s, Sensor = [data_s1[2],data_s2[2],data_s3[2],data_s4[2]], Gas = gas2, Samples = samples[1], Sample_Time = Sample_Time, Path = Path, Gas_Id = gas2_name)

        Gas1 = gas1_name, Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles, Gas1_slopes[0], Gas1_slopes[1], Gas1_slopes[2], Gas1_slopes[3]
        Gas2 = gas2_name, Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, Gas2_slopes[0], Gas2_slopes[1], Gas2_slopes[2], Gas2_slopes[3]



        return Gas1,Gas2

    elif(num_cycle_gas1 > 0):
        print("\n------------------------------------------------------------------------------\n")
        print("Procesando datos. Porfavor, espere...")
        print("\n------------------------------------------------------------------------------\n")

        Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles = get_responses_with_humidity(Sensor = [data_s1[0],data_s2[0],data_s3[0],data_s4[0]],Samples = samples[0], Humidity = humidity)
        Gas1_slopes = get_slopes(Time = t_s, Sensor = [data_s1[0],data_s2[0],data_s3[0],data_s4[0]], Gas = gas1, Samples = samples[0], Sample_Time = Sample_Time, Path = Path, Gas_Id = gas1_name)

        Gas1 = gas1_name, Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles, Gas1_slopes[0], Gas1_slopes[1], Gas1_slopes[2],Gas1_slopes[3]


        return Gas1,0

    elif(num_cycle_gas2 > 0):
        print("\n------------------------------------------------------------------------------\n")
        print("Procesando datos. Porfavor, espere...")
        print("\n------------------------------------------------------------------------------\n")
        Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles = get_responses_with_humidity(Sensor = [data_s1[2],data_s2[2],data_s3[2],data_s4[2]], Samples=samples[1], Humidity = humidity)
        Gas2_slopes = get_slopes(Time = t_s,Sensor = [data_s1[2],data_s2[2],data_s3[2],data_s4[2]], Gas = gas2, Samples = samples[1], Sample_Time = Sample_Time, Path = Path, Gas_Id = gas2_name)

        Gas2 = gas2_name, Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, Gas2_slopes[0], Gas2_slopes[1], Gas2_slopes[2], Gas2_slopes[3]


        return 0,Gas2