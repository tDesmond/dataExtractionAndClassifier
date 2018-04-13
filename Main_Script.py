#
#   Timmy Desmond
#   16/03/2018
#


# Code needs to pull data from csv files (IBI.csv, EDA.csv, Temp.csv)
# Calculations need to be performed on this data to Extract key physiological features
#   Mean Heart Rate
#   Heart Rate Variability (Standard Deviation)
#   Percentage of successive beats that vary by more than 50ms (pNN50)
#   EDA Phasic component (slow moving)
#       Use a moving average on the sample and get the slope to get the general direction of the data
#   EDA Tonic component (slow moving)
#       Use a moving average over longer sample and get direction of data
#   For Temperature we do the same as for EDA
#   Also get Mean value for EDA and Temp
#
# Variables that need to be specified:
#   Time that stress ends and relaxation begins
#   Sample size in seconds
#   csv file names
#   arrays to hold the samples pulled from csv files
#   sample length (the sample lengths will vary as they are specified time windows that will occasionally have missing
#   data)
#   To calculate pnn50 the number of times that the successive peaks vary by more than 50 will need to be counted
#   counted/total = percentage
#   Array for averaged data
#   Array for extracted features to be writing to final csv file
#   Last column on csv file is stressed or not stressed
#       1 for stress and 0 for not stressed

import csv
import numpy as np
from scipy.stats import linregress
from hrv.classical import time_domain
import hrv


def getDataFromCsv(csvFileName, numOfCols):
    print("getDataFromCsv({}, {})".format(csvFileName, numOfCols))

    col_1 = []
    col_2 = []

    with open(csvFileName, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in enumerate(reader):
            if numOfCols == 2:
                if row[0] > 0:
                    col_1.append(round(float(row[1][0]), 3))
                    col_2.append(round(float(row[1][1]), 3))
            elif numOfCols == 1:
                if row[0] > 2:
                    col_2.append(round(float(row[1][0]), 3))
                elif row[0] == 1:
                    sampleRate = float(row[1][0])

    if numOfCols == 1:
        for i in range(len(col_2)):
            col_1.append(i / sampleRate)

    return col_1, col_2


def getSampleWindows(dataSet, times, values):
    print("getSampleWindows({})".format(dataSet))
    window = []
    timeWindows = []
    valueWindows = []

    for i in enumerate(times):
        window.append(i[1])
        # print(window)
        if i[0] > 0:
            # print(window[0], window[-1])

            while ((window[-1] - window[0]) >= 60):
                window.pop(0)
                # print(window[0], window[-1])
                if ((window[-1] - window[0]) <= 60):
                    indexStart = times.index(window[0])
                    indexFinish = times.index(window[-1]) + 1
                    valueWindows.append(values[indexStart:indexFinish])
                    timeWindows.append(window[:])
                    # print(allWindows)

    return timeWindows, valueWindows


def getMeanAndSTD(arrayOfWindows):
    print("getMeanAndSTD()")

    means = []
    std = []
    for i in enumerate(arrayOfWindows):
        means.append(np.mean(i[1]))
        std.append(np.std(i[1]))

    return means, std


def getWindowArray(maxTime):
    initialWindowMax = 60;
    initialWindowMin = 0;
    timeWindowsTemplate = []
    maxTime = int(round(maxTime))

    for i in range(maxTime):
        if i >= 60:
            row = [i - 60, i]
            timeWindowsTemplate.append(row)

    return timeWindowsTemplate;


def getDataWindows(data, times, timeWindows):
    dataWindow = []
    dataWindows = []
    datatimeWindow = []
    datatimeWindows = []

    for i in enumerate(timeWindows):
        indexMn = times.index(i[1][0])
        indexMax = times.index(i[1][1])
        dataWindow = data[indexMn:indexMax]
        dataWindows.append(dataWindow)
        datatimeWindow = times[indexMn:indexMax]
        datatimeWindows.append(datatimeWindow)

    return dataWindows, datatimeWindows


def getEdaSlope(data, time):
    print(data[:200])
    print(time[:200])
    phasicSlope = []
    tonicSlope = []

    # sums = []
    # for i in enumerate(data):
    #     sum = []
    #     print (i[0])
    #     for j in enumerate(i[1]):
    #         print("{} x {}".format((time[0][0]), (data[0][0])))
    #         sum.append((data[i[0]][j[0]]) * time[i[0]][j[0]])
    #     sums.append(sum)

    for i in enumerate(data):
        mPhasic = linregress(time[i[0]][:32], data[i[0]][:32])
        phasicSlope.append(mPhasic.slope)
        mTonic = linregress(time[i[0]], data[i[0]])
        tonicSlope.append(mTonic.slope)

    return phasicSlope, tonicSlope


def getIbiDataWindows(data, times, timeWindows):
    dataWindow = []
    dataWindows = []
    datatimeWindow = []
    datatimeWindows = []

    for i in enumerate(timeWindows):
        firstMinFound = False;
        firstMaxFound = False;
        for j in enumerate(times):
            if (times[j[0]] >= timeWindows[i[0]][0] and (not firstMinFound)):
                indexMn = j[0]
                firstMinFound = True
            if (times[j[0]] >= timeWindows[i[0]][1] and (not firstMaxFound)):
                indexMax = j[0]
                firstMaxFound = True
                dataWindow = data[indexMn:indexMax]
                dataWindows.append(dataWindow)
                datatimeWindow = times[indexMn:indexMax]
                datatimeWindows.append(datatimeWindow)

    # for i in enumerate(timeWindows):
    #     indexMn = times.index(i[1][0])
    #     indexMax = times.index(i[1][1])
    #     dataWindow = [data[indexMn:indexMax]]
    #     dataWindows.append(dataWindow)
    #     datatimeWindow = [times[indexMn:indexMax]]
    #     datatimeWindows.append(datatimeWindow)

    return dataWindows, timeWindows


def main():
    print("main()")
    ibiFileName = "ibi_ibm.csv"
    edaFileName = "eda_ibm.csv"
    # tempFileName = "temp_pres.csv"

    ibiTimes, ibiValues = getDataFromCsv(ibiFileName, 2)
    edaTimes, edaValues = getDataFromCsv(edaFileName, 1)
    # tempTimes, tempValues = getDataFromCsv(tempFileName, 1)

    timeWindows = getWindowArray(edaTimes[-1])

    ibiValueWindows, ibiTimeWindows = getIbiDataWindows(ibiValues, ibiTimes, timeWindows)
    edaValueWindows, edaTimeWindows = getDataWindows(edaValues, edaTimes, timeWindows)
    # tempValueWindows, tempTimeWindows = getDataWindows(tempValues, tempTimes, timeWindows)

    # ibiTimeWindows, ibiValueWindows = getSampleWindows("IBI Data", ibiTimes, ibiValues, timeWindows)
    # edaTimeWindows, edaValueWindows = getSampleWindows("EDA Data", edaTimes, edaValues, timeWindows)
    # tempTimeWindows, tempValueWindows = getSampleWindows("TEMP Data", tempTimes, tempValues, timeWindows)
    #
    ibiMeans, ibiStds = getMeanAndSTD(ibiValueWindows)
    edaMeans, edaStds = getMeanAndSTD(edaValueWindows)
    # tempMeans, tmepStds = getMeanAndSTD(tempValueWindows)

    edaSlopesTonic, edaSlopesPhasic = getEdaSlope(edaValueWindows, edaTimeWindows)

    # print(edaTimeWindows[0])
    print(len(ibiMeans), len(ibiStds))
    print(len(edaMeans), len(edaStds))
    # print(len(tempMeans), len(tmepStds))
    # print(len(edaSlopesPhasic), len(edaSlopesTonic))
    # print(edaMeans)
    # print(edaStds)
    # print(ibiMeans)
    # print(ibiStds)
    # print(tempMeans)
    # print(tmepStds)
    # print(edaSlopesPhasic)
    # print(edaSlopesTonic)

    print(ibiValueWindows[0])
    pnn50Array = []
    for i in ibiValueWindows:
        miliseconds = [x*1000 for x in i];
        # print(miliseconds)
        # print(time_domain(miliseconds)["pnn50"])
        if len(i)>1:
            pnn50Array.append(time_domain(miliseconds)["pnn50"])
        else:
            pnn50Array.append(0)

    print(len(pnn50Array))
    print(len(ibiStds))

    headers = ["IBI Mean", "IBI STD", "pnn50", "EDA Mean", "EDA STD", "EDA Tonic Slope", "EDA Phasic Slope", "Result"]

    with open('ibmExtractedFeatsRaw.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in range(len(edaMeans)):
            if i < len(ibiMeans):
                row = [ibiMeans[i], ibiStds[i], pnn50Array[i], edaMeans[i], edaStds[i], edaSlopesTonic[i], edaSlopesPhasic[i]]
                # print(row)
                writer.writerow(row)


if __name__ == "__main__":
    main()
