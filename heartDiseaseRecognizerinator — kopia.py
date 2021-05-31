import csv
import math

dataPath = "heart.csv"
# dataPath = "dane.csv"
mins, maxs, averages, sigma = [], [], [], 0.1
theDataRow = []


def classify(row):
    """

    :param (one row from a database to compare the New Data to) row:
    :return (similarity with the given database row) result:
    """
    global mins, maxs, averages, sigma
    # the function:
    sum = 0
    for paramIndex, paramValue in enumerate(row[:-1]):
        paramValue = (float(paramValue) - mins[paramIndex]) / (maxs[paramIndex]-mins[paramIndex])
        theDataRowValue = (float(theDataRow[paramIndex]) - mins[paramIndex]) / (maxs[paramIndex]-mins[paramIndex])
        sum += pow(theDataRowValue - paramValue, 2)
        #print("pI: "+str(averages[paramIndex]))
    exponent = - sum / pow(len(row[:-1])*sigma, 2)
    result = math.exp(exponent)
    #print("Sum: "+str(sum))
    #print("Expo: "+str(exponent))
    #print("Res: "+str(result))
    #print(result)
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
            averages[paramIndex] = (averages[paramIndex] - mins[paramIndex]) / (maxs[paramIndex]-mins[paramIndex])
    # for i in mins: print(str(i), end=', ')
    # print()
    # for i in maxs: print(str(i), end=', ')
    # print()
    return


def heartDiseaseRecognizeinator(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    # do sth
    global theDataRow
    theDataRow = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

    normalize()

    resultsSum = [0, 0]         # sum of results/classification probability
    resultsNumbers = [0,0]      # the number of matching results (number of zeroes and ones instances respectively)
    with open(dataPath) as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader, None)  # skipping the header
        for row in csvReader:
            # print(row)
            result = classify(row)
            resultsSum[int(row[-1])] += result
            resultsNumbers[int(row[-1])] += 1
        # print("Results Average: " + str(resultsSum[0]) + ", " + str(resultsSum[1]))
        resultsSum[0] /= resultsNumbers[0]      # making average
        resultsSum[1] /= resultsNumbers[1]      # making average
    print("Results Average: "+str(resultsSum[0])+", "+str(resultsSum[1]))
    if resultsSum[0] > resultsSum[1]:
        return 0
    else:
        return 1


def heartDiseaseBiggerizeinator(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,
                                target):
    # add new row with result
    with open(dataPath, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(
            [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target])
    # printing
    # with open(dataPath) as csvfile:
    #    spamreader = csv.reader(csvfile)
    #    for row in spamreader:
    #        print(', '.join(row))
    return


age = 57
# heartDiseaseRecognizeinator(age,1,0,100,234,0,1,156,0,0.1,2,1,3)    # 0
heartDiseaseRecognizeinator(age,1,0,130,131,0,1,115,1,1.2,1,1,3)    # 0
# heartDiseaseRecognizeinator(age,0,2,130,256,0,0,149,0,0.5,2,0,2)    # 1
# heartDiseaseRecognizeinator(age,1,3,200,564,1,2,202,1,6.2,2,4,3)    # 0
# heartDiseaseBiggerizeinator(age,1,1,120,236,0,1,178,0,0.8,2,0,2,1)
