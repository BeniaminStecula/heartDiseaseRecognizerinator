import csv
import math

dataPath = "heart.csv"
mins, maxs, averages, sigma = [], [], [], 0.1
# averages is currently not used but it's ready for further development
# mins = [29.0, 0.0, 0.0, 94.0, 126.0, 0.0, 0.0, 71.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# maxs = [77.0, 1.0, 3.0, 200.0, 564.0, 1.0, 2.0, 202.0, 1.0, 6.2, 2.0, 4.0, 3.0, 1.0]
theDataRow = []
alternativeResults = 0


def classify(row):
    """
    :param (one row from a database to compare the New Data to) row:
    :return (similarity with the given database row) result:
    """
    global mins, maxs, sigma  # , averages
    # the function:
    sum = 0
    for paramIndex, paramValue in enumerate(row[:-1]):
        paramValue = (float(paramValue) - mins[paramIndex]) / (maxs[paramIndex] - mins[paramIndex])
        theDataRowValue = (float(theDataRow[paramIndex]) - mins[paramIndex]) / (maxs[paramIndex] - mins[paramIndex])
        sum += pow(theDataRowValue - paramValue, 2)
    exponent = - sum / pow(len(row[:-1]) * sigma, 2)
    result = math.exp(exponent)
    return result


def normalize():
    # finding mins and maxs
    global mins, maxs, averages
    rowNumber = 0
    with open(dataPath) as csvFile:
        csvReader = csv.reader(csvFile)
        firstRow = next(csvReader, None)  # skipping the header
        for param in firstRow:
            mins.append(float("inf"))
            maxs.append(0)
            averages.append(0)
        for row in csvReader:
            rowNumber += 1
            for paramIndex, paramValue in enumerate(row):
                if mins[paramIndex] > float(paramValue):
                    mins[paramIndex] = float(paramValue)
                if maxs[paramIndex] < float(paramValue):
                    maxs[paramIndex] = float(paramValue)
                averages[paramIndex] += float(paramValue)
        for paramIndex, paramValue in enumerate(firstRow):
            averages[paramIndex] /= rowNumber
            averages[paramIndex] = (averages[paramIndex] - mins[paramIndex]) / (maxs[paramIndex] - mins[paramIndex])
    # print("Mins: "+ str(mins))
    # print("Maxs: "+ str(maxs))
    return


def heartDiseaseRecognize(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    global theDataRow
    theDataRow = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    global alternativeResults

    normalize()

    resultsSum = [0, 0]  # sum of results/classification probability
    resultsNumbers = [0, 0]  # the number of matching results (number of zeroes and ones instances respectively)
    with open(dataPath) as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader, None)  # skipping the header
        for row in csvReader:
            result = classify(row)
            resultsSum[int(row[-1])] += result
            resultsNumbers[int(row[-1])] += 1

    resultsSum[0] /= resultsNumbers[0]  # making average
    resultsSum[1] /= resultsNumbers[1]  # making average
    alternativeResults = resultsSum[1] / (resultsSum[0] + resultsSum[1]) * 100
    print("Results Alternative:\t" + str(alternativeResults))
    # if resultsSum[0] > resultsSum[1]:
    if alternativeResults < 47:
        print("Results Average:\t" + str(resultsSum[0]) + ",\t" + str(resultsSum[1]) + ",\t0")
        return 0
    else:
        print("Results Average:\t" + str(resultsSum[0]) + ",\t" + str(resultsSum[1]) + ",\t1")
        return 1


def heartDiseaseBiggerize(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                          target):
    # add new row with result
    with open(dataPath, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(
            [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target])
    return


def testOne(target):
    global theDataRow

    result = heartDiseaseRecognize(theDataRow[0], theDataRow[1], theDataRow[2], theDataRow[3], theDataRow[4],
                                   theDataRow[5], theDataRow[6], theDataRow[7], theDataRow[8], theDataRow[9],
                                   theDataRow[10], theDataRow[11], theDataRow[12]) # without target value
    index = 0
    if target == '1': index += 2
    # if result == 1: index += 1
    if alternativeResults >= 47: index += 1
    return index


def testAll():
    recognized = [0, 0, 0, 0]  # should be 0, returned 0; 0:1, 1:0 (dangerous); 1:1
    global theDataRow

    with open(dataPath) as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader, None)  # skipping the header
        for row in csvReader:   # for each row to test call testOne()
            theDataRow = row
            index = testOne(row[-1])
            recognized[index] += 1
    print("Results recognized: " + str(recognized))
    recognizedSum = recognized[0]+recognized[1]+recognized[2]+recognized[3]
    print("Should be 0: " + str(recognized[0]/recognizedSum*100) + "\t" + str(recognized[1]/recognizedSum*100))
    print("Should be 1: " + str(recognized[2]/recognizedSum*100) + "\t" + str(recognized[3]/recognizedSum*100))
    return


# heartDiseaseRecognize(57,1,0,130,131,0,1,115,1,1.2,1,1,3)    # 0
# heartDiseaseRecognize(57,0,2,130,256,0,0,149,0,0.5,2,0,2)    # 1
# heartDiseaseBiggerize(666,1,1,120,236,0,1,178,0,0.8,2,0,2,1)
# testAll()
