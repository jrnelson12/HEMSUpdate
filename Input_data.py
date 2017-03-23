import csv

def inputs_data(day, hour, dfi, dni, ghi, ambtemp, KT, gridPrice, controllableLoad, uncontrollableLoad):
    HemsInputs = open('HemsInputsWeek11.csv', "rt")
    reader = csv.reader(HemsInputs, delimiter=',')
    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            day.append(float(row[0]))
            hour.append(float(row[1]))
            dfi.append(float(row[2]))
            dni.append(float(row[3]))
            ghi.append(float(row[4]))
            ambtemp.append(float(row[5]))
            KT.append(float(row[6]))
            gridPrice.append(float(row[7]))
            controllableLoad.append(float(row[8]))
            uncontrollableLoad.append(float(row[9]))
        rownum += 1
    HemsInputs.close()
    return day, hour, dfi, dni, ghi, ambtemp, KT, gridPrice, controllableLoad, uncontrollableLoad