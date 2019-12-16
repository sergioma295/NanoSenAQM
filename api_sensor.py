import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
import numpy as np


class Measure():
    """ Measure class. We use this as a public class example class. It has the necessary methods to process the
    previously created file

    *** Note: You never call this class before create a file object.***

    """

    def __init__(self, file):
        self.file =  file
        self.data = file.getData()

    def readSampleTime(self):
        """
           Method to read the sample time in the measure.
        """
        t_s = self.data['Tiempo_segundos']

        # Obtaining the sample time and storing it in a list
        sample_time = []
        for index in range(len(t_s)-1):
            s_t = t_s[index+1] - t_s[index]
            sample_time.append(s_t)

        # Check that the sample time has the same length -1 as the time series
        if(len(sample_time)==len(t_s)-1):
            pass
        else:
            print("[INFO] Error. Sample Time.")

        self.sample_time = sample_time
        self.sample_time_mean = getStatistics(sample_time,'Sample Time',0)

    def getSampleTime(self):
        """
        Method to get the sample time processed\n
        :return: sample_time
        :rtype: float
        """
        return self.sample_time

    def getSampleTimeMean(self):
        """
        Method to get the sample time mean\n
        :return: sample_time_mean
        :rtype: float
        """
        return self.sample_time_mean

    def readGasesCycles(self):
        """
        Method to read the different gas cyles in order to obtain the index where concentration changes.

        """
        gasesId = self.file.getIdGases()
        gas1 = self.data[gasesId[0]]
        gas2 = self.data[gasesId[1]]
        # Creation of two types of variables to store the indices and the number of cycles of each gas
        num_cycle_gas1 = 0
        num_cycle_gas2 = 0
        gas1_index = [0]
        gas2_index = [0]
        for index in range(len(gas1) - 1):
            if (gas1[index + 1] == gas1[index] or np.math.isnan(gas1[index + 1])):
                pass
            else:
                gas1_index.append(index)

                num_cycle_gas1 += 1

            if (gas2[index + 1] == gas2[index] or np.math.isnan(gas2[index + 1])):
                pass
            else:
                gas2_index.append(index)
                num_cycle_gas2 += 1

        # Add the last leg.
        gas1_index.append(len(gas1) - 1)
        gas2_index.append(len(gas2) - 1)

        # Number of measurement cycles.
        num_cycle_gas1 /= 2
        num_cycle_gas2 /= 2

        # Save as variable class.
        self.num_cycle_gas1 = num_cycle_gas1
        self.num_cycle_gas2 = num_cycle_gas2
        self.gas1_index = gas1_index
        self.gas2_index = gas2_index

    def getGasesCycles(self):
        """
        Method to get the gas cycle variables\n
        :return: number_of_cycles_gas1, number_of_cycles_gas2, gas1_index, gas2_index
        :rtype: int, int, list, list
        """
        return self.num_cycle_gas1,self.num_cycle_gas2, self.gas1_index, self.gas2_index

    def getNumCycleGas(self):
        """
        Method to get the gas cycle number\n
        :return: number_of_cycles_gas1, number_of_cycles_gas2
        :rtype: int, int
        """
        return self.num_cycle_gas1,self.num_cycle_gas2

    def getIndexCycleGas(self):
        """
        Method to get the gas cycle index\n
        :return: gas1_index, gas2_index
        :rtype: list, list
        """
        return self.gas1_index, self.gas2_index

    def getGases(self):
        """
        Method to get the gases name\n
        :return: gas1_name, gas2_name
        :rtype: str, str
        """
        gasId = self.file.getIdGases()
        return self.data[gasId[0]], self.data[gasId[1]]

    def getSimpleGas(self, gasId):
        """
        Method to get a gas name\n
        :return: gasX_name
        :rtype: str
        """
        return self.data[gasId]

    def getSensor(self):
        """
        Method to get the sensor values\n
        :return: [s1,s2,s3,s4]
        :rtype: list
        """
        s1 = self.data['S1'].tolist()
        s2 = self.data['S2'].tolist()
        s3 = self.data['S3'].tolist()
        s4 = self.data['S4'].tolist()
        return [s1, s2, s3, s4]

    def getTime(self):
        """
        Method to get the time variable of measure\n
        :return: time_(seconds)
        :rtype: list
        """
        t_s = self.data['Tiempo_segundos']
        return t_s

    def getHumidity(self):
        """
        Method to get the humidity variable of measure\n
        :return: humidity(%)
        :rtype: list
        """
        humidity = self.data['Humidity'].tolist()
        return humidity

    def getVoltageHeaters(self):
        """
        Method to get the voltage variable of measure\n
        :return: voltage(mV)
        :rtype: list
        """
        V1 = self.data['V1'].tolist()
        V2 = self.data['V2'].tolist()
        V3 = self.data['V3'].tolist()
        V4 = self.data['V4'].tolist()

        return [V1,V2,V3,V4]

    def getDatafromMeasure(self):
        """
        Method to get all data in this measure
        :return: data
        :rtype: DataFrame
        """
        return self.data

    def readCyclesData(self,Gas, Index):
        """
        Method to read data of every Cycle getting variables list with a number of elements equal to number of cycle gas\n

        """
        Sensor = self.getSensor()
        # Variable to store the indices of each cycle
        samples = []
        # Getting Time
        t_s_value = self.getTime().tolist()
        t_s = []
        # Temporary variables to store the resistance value of the sensors.
        s1 = Sensor[0]
        s2 = Sensor[1]
        s3 = Sensor[2]
        s4 = Sensor[3]

        # Method Output Variables
        data_s1 = []
        data_s2 = []
        data_s3 = []
        data_s4 = []
        data_gas = []

        # We scroll the list with the indexes that indicate a change of concentration
        for index in range(len(Index)):
            # We check if the index is odd or its value is greater than the length of the number of concentration changes
            # minus three. Otherwise, we add to the vector the resistances from this index to this index + 3.
            if index % 2 != 0 or index > (len(Index) - 3):
                pass
            else:
                # Calculation of indexes for the lower limit and the upper limit.
                lim_inf = Index[index]
                lim_sup = Index[index + 3]

                # Obtaining gas concentration
                gas = Gas[lim_inf:lim_sup]

                # Variable that stores the indexes of each cycle
                samples.append(Index[index:(index + 4)])

                # Obtaining the values between the limits for each sensor.
                # SENSOR 1
                s1_ = s1[lim_inf:lim_sup]

                # SENSOR 2
                s2_ = s2[lim_inf:lim_sup]

                # SENSOR 3
                s3_ = s3[lim_inf:lim_sup]

                # SENSOR 4
                s4_ = s4[lim_inf:lim_sup]

                # Time
                t_s_ = t_s_value[lim_inf:lim_sup]

                data_s1.append(s1_)
                data_s2.append(s2_)
                data_s3.append(s3_)
                data_s4.append(s4_)
                data_gas.append(gas)
                t_s.append(t_s_)

        self.dataS1  = data_s1
        self.dataS2  = data_s2
        self.dataS3  = data_s3
        self.dataS4  = data_s4
        self.dataGas = data_gas
        self.samples = samples
        self.t_s_steps = t_s
        self.index = Index # CAMBIO

    def getTsSteps(self):
        """
        Method to return t_s list[cycle1, cycle2,...,cyclen]
        :return: t_s_steps
        :rtype: list[cycle_i, ..., cycle_n]
        """
        return self.t_s_steps

    def getCyclesData(self):
        return self.dataS1, self.dataS2, self.dataS3, self.dataS4, self.dataGas, self.samples

    def readSamplesCycles(self):
        """
        Method to read data in every cycle generating an output list where\n
        1. Element 0 are sensor values gas 1.
        2. Element 1 are gas 1 values.
        3. Element 2 are sensor values gas 2.
        4. Element 3 are gas 2 values.\n

        """
        # The variables NO2 and CO are converted to List.
        gases = self.getGases()
        gas1 = gases[0].tolist()
        gas2 = gases[1].tolist()
        # Getting Time
        # t_s = self.getTime()
        # We get the indices
        index = self.getIndexCycleGas()
        index1 = index[0]
        index2 = index[1]

        # Variables for storing gas data
        GAS1 = 0
        GAS2 = 0

        # A cycle contains all points from the Pt.A - Pt.D

        #                                       ----------------
        #                                       |              |
        #                                       |              |
        #                           ------------|              |----------
        #                           Pt.A        Pt.B          Pt.C       Pt.D

        # If the length of variable no2_index or co_index > 2, there are cycles. In cc there are NO cycles and this variable
        # it will only have two occupied positions, the initial and final value of that experiment.
        if (len(index1) != 2):
            self.readCyclesData(Gas=gas1,Index=index1)
            S1_GAS1, S2_GAS1, S3_GAS1, S4_GAS1, GAS1, GAS1_samples = self.getCyclesData()

        if (len(index2) != 2):
            self.readCyclesData(Gas=gas2,Index=index2)
            S1_GAS2, S2_GAS2, S3_GAS2, S4_GAS2, GAS2, GAS2_samples = self.getCyclesData()

        if (GAS1) != 0 and GAS2 != 0:
            # Grouping of sensor and gas data
            data_s1 = [S1_GAS1, GAS1, S1_GAS2, GAS2]
            data_s2 = [S2_GAS1, GAS1, S2_GAS2, GAS2]
            data_s3 = [S3_GAS1, GAS1, S3_GAS2, GAS2]
            data_s4 = [S4_GAS1, GAS1, S4_GAS2, GAS2]

        elif (GAS1 != 0):
            # Grouping of sensor and gas data
            # Copy and initialize to 0 the output always maintain the same structure
            GAS2 = [[0 for i in range(len(GAS1[0]))] for j in range(len(GAS1))]

            S1_GAS2 = [[0 for i in range(len(S1_GAS1[0]))] for j in range(len(S1_GAS1))]
            S2_GAS2 = [[0 for i in range(len(S2_GAS1[0]))] for j in range(len(S2_GAS1))]
            S3_GAS2 = [[0 for i in range(len(S3_GAS1[0]))] for j in range(len(S3_GAS1))]
            S4_GAS2 = [[0 for i in range(len(S4_GAS1[0]))] for j in range(len(S4_GAS1))]

            data_s1 = [S1_GAS1, GAS1, S1_GAS2, GAS2]
            data_s2 = [S2_GAS1, GAS1, S2_GAS2, GAS2]
            data_s3 = [S3_GAS1, GAS1, S3_GAS2, GAS2]
            data_s4 = [S4_GAS1, GAS1, S4_GAS2, GAS2]

            # We copy and initialize to 0 the value of GAS2_samples so that the output always maintains the same structure.
            GAS2_samples = [[0 for i in range(len(GAS1_samples[0]))] for j in range(len(GAS1_samples))]


        elif (GAS2 != 0):
            # Grouping of sensor and gas data
            # Copy and initialize to 0 the output always maintain the same structure
            GAS1 = [[0 for i in range(len(GAS2[0]))] for j in range(len(GAS2))]

            S1_GAS1 = [[0 for i in range(len(S1_GAS2[0]))] for j in range(len(S1_GAS2))]
            S2_GAS1 = [[0 for i in range(len(S2_GAS2[0]))] for j in range(len(S2_GAS2))]
            S3_GAS1 = [[0 for i in range(len(S3_GAS2[0]))] for j in range(len(S3_GAS2))]
            S4_GAS1 = [[0 for i in range(len(S4_GAS2[0]))] for j in range(len(S4_GAS2))]

            data_s1 = [S1_GAS1, GAS1, S1_GAS2, GAS2]
            data_s2 = [S2_GAS1, GAS1, S2_GAS2, GAS2]
            data_s3 = [S3_GAS1, GAS1, S3_GAS2, GAS2]
            data_s4 = [S4_GAS1, GAS1, S4_GAS2, GAS2]

            # We copy and initialize to 0 the value of GAS2_samples so that the output always maintains the same structure.
            GAS1_samples = [[0 for i in range(len(GAS2_samples[0]))] for j in range(len(GAS2_samples))]

        samples = GAS1_samples, GAS2_samples

        self.data_s1 = data_s1
        self.data_s2 = data_s2
        self.data_s3 = data_s3
        self.data_s4 = data_s4
        self.samples = samples

    def getSamplesCycles(self,gasId):
        """

        :param gasId: Id to return data.\n
        If gasId=1 return gas1 data.\n
        If gasId=2 return gas2 data.\n
        If gasId=3 return gas1 and gas2 data.\n
        """
        if(gasId==1):
            a1 = [self.data_s1[gasId-1],self.data_s1[gasId]]
            a2 = [self.data_s2[gasId-1],self.data_s2[gasId]]
            a3 = [self.data_s3[gasId-1],self.data_s3[gasId]]
            a4 = [self.data_s4[gasId-1],self.data_s4[gasId]]
            a5 = self.samples[gasId - 1]
            return a1,a2,a3,a4,a5
        elif(gasId==2):
            a1 = [self.data_s1[gasId],self.data_s1[gasId+1]]
            a2 = [self.data_s2[gasId],self.data_s2[gasId+1]]
            a3 = [self.data_s3[gasId],self.data_s3[gasId+1]]
            a4 = [self.data_s4[gasId],self.data_s4[gasId+1]]
            a5 = self.samples[gasId - 1]
            return a1,a2,a3,a4,a5
        elif(gasId==3):
            return self.data_s1, self.data_s2, self.data_s3, self.data_s4, self.samples
        else:
            print("[INFO] Error. Command not specified <<getSamplesCycles(self,id) id != 1,2,3>>")


    def readResponse(self, gasId):
        """
        Method to read response in every cycle.\n
        :param gasId: It is of the gas to be read with the method <<self.getSamplesCycles(gasId)>>
        """
        s1, s2, s3, s4, samples  = self.getSamplesCycles(gasId=gasId)
        gas = self.getGases()[gasId-1].tolist()
        s1 = s1[0]
        s2 = s2[0]
        s3 = s3[0]
        s4 = s4[0]
        # Getting humidity
        humidity = self.getHumidity()
        # Getting Voltage of Heaters
        voltage = self.getVoltageHeaters()
        # Initialization of the variables where the answers will be added.
        rs1 = []
        rs2 = []
        rs3 = []
        rs4 = []
        hum = []
        v1  = []
        v2  = []
        v3  = []
        v4  = []
        gas_ = []
        for index in range(len(samples)):
            # We get the resistance indices to get the answer. The indices are calculated as:
            # For the Rair, we subtract the value of the second element with the first one.
            # For Rgas, subtract the value of the third element with the second and add the Rair.
            Rair_index = samples[index][1] - samples[index][0]
            Rgas_index = samples[index][2] - samples[index][1] + Rair_index

            # Getting Answers S1
            Rair = s1[index][Rair_index]
            Rgas = s1[index][Rgas_index]
            Rs1 = Rgas / Rair
            rs1.append(Rs1)

            # Getting Answers S2
            Rair = s2[index][Rair_index]
            Rgas = s2[index][Rgas_index]

            Rs2 = Rgas / Rair
            rs2.append(Rs2)

            # Getting Answers S3
            Rair = s3[index][Rair_index]
            Rgas = s3[index][Rgas_index]

            Rs3 = Rgas / Rair
            rs3.append(Rs3)

            # Getting Answers S4
            Rair = s4[index][Rair_index]
            Rgas = s4[index][Rgas_index]

            Rs4 = Rgas / Rair
            rs4.append(Rs4)

            # We calculate the average humidity in the presence of the gas.
            lim_hum_sup = int(samples[index][2])
            lim_hum_inf = int(samples[index][1])
            temp_hum = humidity[lim_hum_inf:lim_hum_sup]
            # Voltage
            temp_V1 = voltage[0][lim_hum_inf:lim_hum_sup]  # V1
            temp_V2 = voltage[1][lim_hum_inf:lim_hum_sup]  # V2
            temp_V3 = voltage[2][lim_hum_inf:lim_hum_sup]  # V3
            temp_V4 = voltage[3][lim_hum_inf:lim_hum_sup]  # V4
            # Humidity Mean in these cycle
            hum_mean = getStatistics(temp_hum, 'Humidity', 0)
            # Voltage Means in these cycle
            V1_mean  = getStatistics(temp_V1, 'V1', 0)
            V2_mean  = getStatistics(temp_V2, 'V2', 0)
            V3_mean  = getStatistics(temp_V3, 'V3', 0)
            V4_mean  = getStatistics(temp_V4, 'V4', 0)

            gas_mean = getStatistics(gas[samples[index][1]+1:samples[index][2]], 'Gas Concentration', 0)
            hum.append(hum_mean)

            v1.append(V1_mean)
            v2.append(V2_mean)
            v3.append(V3_mean)
            v4.append(V4_mean)

            gas_.append(gas_mean)

        self.rs1 = rs1
        self.rs2 = rs2
        self.rs3 = rs3
        self.rs4 = rs4
        self.hum = hum
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.gas_ = gas_

    def getVoltage(self):
        """
        Return voltage value of heaters in every cycle of gas
        :return: v1,v2,v3,v4
        """
        return self.v1, self.v2, self.v3, self.v4

    def getResponse(self):
        """
        Method to get the response read.\n
        :return: response_S1, response_S2, response_S3, response_S4, V1, V2, V3, V4
        :rtype: list, list, list, list, list, list, list, list
        """
        return self.rs1, self.rs2, self.rs3, self.rs4, self.hum, self.v1, self.v2, self.v3, self.v4, self.gas_

    def readSlopes(self, gasName, gasId):
        """
        Method to read the 3 slopes within gas cycle.\n
        :param gasName: It's the name of the gas to be read
        :param gasId: It is of the gas to be read with the method <<self.getSamplesCycles(gasId)>>
        """
        t = self.getTime()
        s1, s2, s3, s4, samples  = self.getSamplesCycles(gasId=gasId)
        # Sensor Data
        s1 = s1[0]
        s2 = s2[0]
        s3 = s3[0]
        s4 = s4[0]
        # Sample time
        sampleTime = self.getSampleTimeMean()
        # Path to store generated images
        path = self.file.getPathImages()
        # Gas concentration data
        gas = self.getSimpleGas(gasName).tolist()


        # Variable for storing slopes
        slope1 = []  # Variable para almacenar pendientes del sensor 1
        slope2 = []  # Variable para almacenar pendientes del sensor 2
        slope3 = []  # Variable para almacenar pendientes del sensor 3
        slope4 = []  # Variable para almacenar pendientes del sensor 4

        for index in range(len(samples)):
            # We obtain the resistance indices that are found within the cycle, that is, in the presence of a gas
            # pollutant.
            # These limits are calculated to be used in the resistance array
            lim_inf_G = samples[index][1]
            lim_sup_G = samples[index][2]

            # These limits are calculated to be used in the time array and gas concentration
            lim_inf_R = samples[index][1] - samples[index][0]
            lim_sup_R = samples[index][2] - samples[index][1] + lim_inf_R

            # We get the cycle width (number of points). We divide in three the total of points to obtain three sections
            num_samples = (lim_sup_R - lim_inf_R) / 3

            # We get indexes tranches
            # STEP 1
            # Resistance
            tramo1_inf_R = int(lim_inf_R)
            tramo1_sup_R = int(tramo1_inf_R + num_samples)

            # Time and Concentration
            tramo1_inf_G = int(lim_inf_G)
            tramo1_sup_G = int(tramo1_inf_G + num_samples)

            # STEP 2
            tramo2_inf_R = int(tramo1_sup_R)
            tramo2_sup_R = int(tramo2_inf_R + num_samples)

            # Time and Concentration
            tramo2_inf_G = int(tramo1_sup_G)
            tramo2_sup_G = int(tramo2_inf_G + num_samples)

            # STEP 3
            tramo3_inf_R = int(tramo2_sup_R)
            tramo3_sup_R = int(tramo3_inf_R + num_samples)

            # Time and Concentration
            tramo3_inf_G = int(tramo2_sup_G)
            tramo3_sup_G = int(tramo3_inf_G + num_samples)

            # Obtaining the time value in each section
            # STEP 1
            t1_1 = t[tramo1_inf_G]  # T1 en tramo 1
            t2_1 = t[tramo1_sup_G]  # T2 en tramo 1

            # STEP 2
            t1_2 = t[tramo2_inf_G]  # T1 en tramo 2
            t2_2 = t[tramo2_sup_G]  # T2 en tramo 2

            # STEP 3
            t1_3 = t[tramo3_inf_G]  # T1 en tramo 3
            t2_3 = t[tramo3_sup_G]  # T2 en tramo 3

            # Plot step. Lower limit for the whole period
            a = samples[index][0]
            b = samples[index][3]

            # Obtaining the value of the resistance in each section. Included in the function is the calculation of the slope and
            # its representation with the aim of making the program modular. Next we repeat the call to the
            # "process Earrings" function for each sensor we have.

            # SENSOR 1
            slope_, n_ = procesarPendientes(s1, index,
                                             t1_1, t2_1,
                                             t1_2, t2_2,
                                             t1_3, t2_3,
                                             tramo1_inf_R, tramo1_sup_R,
                                             tramo2_inf_R, tramo2_sup_R,
                                             tramo3_inf_R, tramo3_sup_R)

            slope1.append(slope_)

            # We put a title to the figure and to the file to save it
            # We put a title to the figure and to the file to save it
            title = 'Slope_S1_Cycle_' + str(index + 1) + '_' + gasName
            path_ = path + 'Slopes/S1/' + title + '.png'
            plotSlope(Time=t[a:b], Sensor=s1[index], Gas=gas[a:b], Time_Final=[t2_1, t2_2, t2_3],
                             Time_Initial=[t1_1, t1_2, t1_3], Sample_Time=sampleTime, Slope=slope_, N=n_, Path=path_,
                             Title=title, Id=gasId)

            # SENSOR 2
            slope_, n_ = procesarPendientes(s2, index,
                                             t1_1, t2_1,
                                             t1_2, t2_2,
                                             t1_3, t2_3,
                                             tramo1_inf_R, tramo1_sup_R,
                                             tramo2_inf_R, tramo2_sup_R,
                                             tramo3_inf_R, tramo3_sup_R)

            slope2.append(slope_)

            title = 'Slope_S2_Cycle_' + str(index + 1) + '_' + gasName
            path_ = path + 'Slopes/S2/' + title + '.png'
            plotSlope(Time=t[a:b], Sensor=s2[index], Gas=gas[a:b], Time_Final=[t2_1, t2_2, t2_3],
                             Time_Initial=[t1_1, t1_2, t1_3], Sample_Time=sampleTime, Slope=slope_, N=n_, Path=path_,
                             Title=title, Id=gasId)

            # SENSOR 3
            slope_, n_ = procesarPendientes(s3, index,
                                             t1_1, t2_1,
                                             t1_2, t2_2,
                                             t1_3, t2_3,
                                             tramo1_inf_R, tramo1_sup_R,
                                             tramo2_inf_R, tramo2_sup_R,
                                             tramo3_inf_R, tramo3_sup_R)

            slope3.append(slope_)

            title = 'Slope_S3_Cycle_' + str(index + 1) + '_' + gasName
            path_ = path + 'Slopes/S3/' + title + '.png'
            plotSlope(Time=t[a:b], Sensor=s3[index], Gas=gas[a:b], Time_Final=[t2_1, t2_2, t2_3],
                             Time_Initial=[t1_1, t1_2, t1_3], Sample_Time=sampleTime, Slope=slope_, N=n_, Path=path_,
                             Title=title, Id=gasId)

            # SENSOR 4
            slope_, n_ = procesarPendientes(s4, index,
                                             t1_1, t2_1,
                                             t1_2, t2_2,
                                             t1_3, t2_3,
                                             tramo1_inf_R, tramo1_sup_R,
                                             tramo2_inf_R, tramo2_sup_R,
                                             tramo3_inf_R, tramo3_sup_R)

            slope4.append(slope_)

            title = 'Slope_S4_Cycle_' + str(index + 1) + '_' + gasName
            path_ = path + 'Slopes/S4/' + title + '.png'
            plotSlope(Time=t[a:b], Sensor=s4[index], Gas=gas[a:b], Time_Final=[t2_1, t2_2, t2_3],
                             Time_Initial=[t1_1, t1_2, t1_3], Sample_Time=sampleTime, Slope=slope_, N=n_, Path=path_,
                             Title=title, Id=gasId)

        self.slope1 = slope1
        self.slope2 = slope2
        self.slope3 = slope3
        self.slope4 = slope4

    def getSlopes(self):
        """
        Method to get the slope processed.\n
        :return: slope_S1, slope_S2, slope_S3, slope_S4
        :rtype: list, list, list, list
        """
        return [self.slope1, self.slope2, self.slope3, self.slope4]

    def readCharacteristics(self):
        """
        Method to read Characteristics of the Measure, such us, response, adsorption and desorption time (not yet implemented), temperatures, slopes etc.
        """
        gasId = self.file.getIdGases()
        sampleTime = self.getSampleTimeMean()

        # We save each parameter in a variable
        t_s = self.data['Tiempo_segundos']
        gas1 = self.data[gasId[0]]
        gas2 = self.data[gasId[1]]
        gas1_name = gasId[0]  # Nombre Gas 1
        gas2_name = gasId[1]  # Nombre Gas 2
        humidity = self.data['Humidity'].tolist()
        # We get those indices and number of cycads.
        self.readGasesCycles()
        num_cycle_gas1, num_cycle_gas2, gas1_index, gas2_index = self.getGasesCycles()
        # We obtain the points corresponding to each cycle.
        self.readSamplesCycles()
        data_s1, data_s2, data_s3, data_s4, samples = self.getSamplesCycles(gasId=3)
        # We get the answers corresponding to each cycle for the given gas
        # In the first place it is checked with how many gases have been worked.
        if (num_cycle_gas1 > 0 and num_cycle_gas2 > 0):
            print("\n------------------------------------------------------------------------------\n")
            print("[INFO] Processing data. Please wait...")
            print("\n------------------------------------------------------------------------------\n")

            self.readResponse(gasId=1)
            Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles, V1_1, V2_1, V3_1, V4_1, GasConcentration1 = self.getResponse()

            self.readResponse(gasId=2)
            Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, V1_2, V2_2, V3_2, V4_2, GasConcentration2 = self.getResponse()


            # We calculate the slopes of each cycle and store them in a variable
            # Gas 1
            self.readSlopes(gasName=gas1_name, gasId=1)
            Gas1_slopes = self.getSlopes()

            # Gas2
            self.readSlopes(gasName=gas2_name, gasId=2)
            Gas2_slopes = self.getSlopes()

            # Creation of the variable characteristics
            Gas1 = gas1_name, Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles, Gas1_slopes[0], Gas1_slopes[
                1], Gas1_slopes[2], Gas1_slopes[3], V1_1, V2_1, V3_1, V4_1, GasConcentration1
            Gas2 = gas2_name, Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, Gas2_slopes[0], Gas2_slopes[
                1], Gas2_slopes[2], Gas2_slopes[3], V1_2, V2_2, V3_2, V4_2, GasConcentration2

            self.Gas1 = Gas1
            self.Gas2 = Gas2

        elif (num_cycle_gas1 > 0):
            print("\n------------------------------------------------------------------------------\n")
            print("[INFO] Processing data. Please wait...")
            print("\n------------------------------------------------------------------------------\n")

            # Reading of the answer in each cycle, we obtain results and store in variables.
            self.readResponse(gasId=1)
            Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, Gas1_humidity_cycles, V1, V2, V3, V4, GasConcentration = self.getResponse()

            # We calculate the slopes and store them in a variable
            self.readSlopes(gasName=gas1_name, gasId=1)
            Gas1_slopes = self.getSlopes()

            # Creation of the variable characteristics
            Gas1 = gas1_name, \
                   Gas1_rs1, Gas1_rs2, Gas1_rs3, Gas1_rs4, \
                   Gas1_humidity_cycles, \
                   Gas1_slopes[0], Gas1_slopes[1], Gas1_slopes[2], Gas1_slopes[3],\
                   V1, V2, V3,V4, \
                   GasConcentration

            self.Gas1 = Gas1
            self.Gas2 = 0


        elif (num_cycle_gas2 > 0):
            print("\n------------------------------------------------------------------------------\n")
            print("Procesando datos. Porfavor, espere...")
            print("\n------------------------------------------------------------------------------\n")
            # Reading of the answer in each cycle, we obtain results and store in variables.
            self.readResponse(gasId=2)
            Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, V1, V2, V3, V4, GasConcentration = self.getResponse()

            # We calculate the slopes and store them in a variable
            self.readSlopes(gasName=gas2_name, gasId=2)
            Gas2_slopes = self.getSlopes()

            # Creation of the variable characteristics
            Gas2 = gas2_name, Gas2_rs1, Gas2_rs2, Gas2_rs3, Gas2_rs4, Gas2_humidity_cycles, Gas2_slopes[0], Gas2_slopes[
                1], Gas2_slopes[2], Gas2_slopes[3], V1, V2, V3, V4, \
                   GasConcentration

            self.Gas1 = 0
            self.Gas2 = Gas2

    def getCharacteristics(self):
        """
        Method to get the characteristics processed.
        :return: Gas1, Gas2
        :rtype: list, list
        """
        return self.Gas1, self.Gas2, self.index # CAMBIO self.index


def getStatistics(variable,name, output):
    """
    Method to apply different statistics formulas, such as, mean, var etc. Depend on the output variable return one or other.

    """
    # We converted from List to DataFrame
    data_frame = pd.DataFrame(variable)

    if (output ==0):
        media = data_frame.mean().values[0]  # Arithmetic mean
        return media
    elif( output == 1):
        media_geometrica = stats.gmean(data_frame)[0]  # Geometric mean
        return media_geometrica

    elif (output == 3):
        media_armonica = stats.hmean(data_frame)[0]  # Harmonic mean
        return media_armonica

    elif (output == 4):
        mediana = data_frame.median().values[0]  # Median
        return mediana

    elif (output == 5):
        moda = data_frame.mode().values[0][0]  # Trendy
        return moda

    elif (output == 6):
        varianza = data_frame.var().values[0]  # Variance
        return varianza

    elif (output == 7):
        varianza_estandar = data_frame.std().values[0]  # Standar Variance
        return varianza_estandar

    elif (output == 8):
        descripcion_estadistica = data_frame.describe()
        return descripcion_estadistica
    else:
        print("[INFO] Error. Statistical resume")

def calculateSlope(r2,r1, t2,t1):
    """
    Method to calculate slope of a specific step.\n
    :param r2: final resistance
    :param r1: initial resistances
    :param t2: final time
    :param t1: initial time
    :return: slope. (r2-r1)/(t2-t1)
    :rtype: float
    """
    incResistencia = r2 - r1
    incTiempo = t2 - t1

    m = (incResistencia) / incTiempo
    n = r2 - m*t2

    return m,n

def plotSlope(Time, Sensor,Gas, Time_Final, Time_Initial,Sample_Time, Slope, N,Path, Title, Id):
    """
    Method to plot the slopes calculated.\n
    :param Time: time variable
    :param Sensor: sensor data
    :param Gas: gas data
    :param Time_Final: Final time data
    :param Time_Initial: Initial Time data
    :param Sample_Time: Sample time Mean calculated
    :param Slope: Slope calculated
    :param N: n value of line (y=slope*x+N)
    :param Path: Path to be stored
    :param Title: Title to be stored
    :param Id: Gas id
    """
    time = Time.tolist()
    a = len(Sensor)
    b = len(time)
    # We get the previously calculated limit values for each leg
    # STEP 1
    tf1 = Time_Final[0]
    ti1 = Time_Initial[0]

    # STEP 2
    tf2 = Time_Final[1]
    ti2 = Time_Initial[1]

    # STEP 3
    tf3 = Time_Final[2]
    ti3 = Time_Initial[2]

    # We get the slopes of the three sections
    # STEP 1
    m1 = Slope[0]
    n1 = N[0]
    # We calculate the line to represent it
    x1 = np.linspace(int(ti1),int(tf1),int(Sample_Time))
    y1 = m1*x1 + n1

    # STEP 2
    m2 = Slope[1]
    n2 = N[1]
    # We calculate the line to represent it
    x2 = np.linspace(int(ti2),int(tf2),int(Sample_Time))
    y2 = m2*x2 + n2

    # STEP 3
    m3 = Slope[2]
    n3 = N[2]
    # We calculate the line to represent it
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

def procesarPendientes(sensor,index,t1_1,t2_1,t1_2,t2_2,t1_3,t2_3,tramo1_inf_R, tramo1_sup_R,tramo2_inf_R, tramo2_sup_R,tramo3_inf_R, tramo3_sup_R):
    """
    Method to calculate the three slopes in a specific cycle.\n
    :param sensor: Sensor data
    :param index:  Index of data in a specific cycle
    :param t1_1:  time1_1. Time 1 step 1
    :param t2_1:  time2_1. Time 2 step 2
    :param t1_2:  time1_2. Time 1 step 2
    :param t2_2:  time2_2. Time 2 step 2
    :param t1_3:  time1_3. Time 1 step 3
    :param t2_3:  time2_3. Time 2 step 3
    :param tramo1_inf_R: Value of resistance inf in step 1
    :param tramo1_sup_R: Value of resistance sup in step 1
    :param tramo2_inf_R: Value of resistance inf in step 2
    :param tramo2_sup_R: Value of resistance sup in step 2
    :param tramo3_inf_R: Value of resistance inf in step 3
    :param tramo3_sup_R: Value of resistance sup in step 3
    :return: m, n
    :rtype: list, list
    """
    r1_1_1 = sensor[index][tramo1_inf_R]  # Sensor point S1, 1 in section 1
    r1_2_1 = sensor[index][tramo1_sup_R]  # Sensor point S1, 2 in section 1

    r1_1_2 = sensor[index][tramo2_inf_R]  # Sensor point S1, 1 in section 2
    r1_2_2 = sensor[index][tramo2_sup_R]  # Sensor point S1, 2 in section 2

    r1_1_3 = sensor[index][tramo3_inf_R]  # Sensor point S1, 1 in section 3
    r1_2_3 = sensor[index][tramo3_sup_R]  # Sensor point S1, 2 in section 3

    # Calculation of slope (increaseResistance / increaseTime) in each section
    # STEP 1
    m1, n1 = calculateSlope(r1_2_1, r1_1_1, t2_1, t1_1)

    # STEP 2
    m2, n2 = calculateSlope(r1_2_2, r1_1_2, t2_2, t1_2)

    # STEP 3
    m3, n3 = calculateSlope(r1_2_3, r1_1_3, t2_3, t1_3)

    slope_ = [m1, m2, m3]
    n_     = [n1, n2, n3]

    return slope_, n_

