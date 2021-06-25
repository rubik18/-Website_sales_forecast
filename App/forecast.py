import os
import pandas as pd
import matplotlib.pyplot as plt

c = pd.read_csv("../data/fptshop.csv")

global d
d = list(c[c["Provinces"] == "Hà Nội"]["Code"])


def SaleShopWeek(data, MaSP, MaShop):
    data['date'] = pd.to_datetime(data['date'])
    data['week'] = data['date'].apply(lambda x: x.isocalendar()[1])
    result = data[(data['shop'] == MaShop) & (data['item'] == str(MaSP)) & (data["status"] == "F")& (data['qty'] <= 3)]
    # print(result)
    arr = list(result['week'])
    dic = {}
    for x in arr:
        re = result[result['week'] == x]
        dic[x] = sum(re['qty'])
    return dic


def SaleProvinceWeek(data, MaSP, ListShop):
    data['date'] = pd.to_datetime(data['date'])
    data['week'] = data['date'].apply(lambda x: x.isocalendar()[1])
    result = data[(data['shop'].isin(ListShop)) & (data['item'] == str(MaSP)) & (data["status"] == "F") & (data['qty'] <= 3)]
    arr = list(result['week'])
    dic = {}
    for x in arr:
        re = result[result['week'] == x]
        dic[x] = sum(re['qty'])
    return dic


def merge_dicts(dict1, dict2):
    for k, v in dict2.items():
        if k in dict1:
            dict1[k] += v
        else:
            dict1[k] = v

    return dict1


def error(forecast, real):
    neg, pos = 0, 0
    er = {key: real[key] - forecast.get(key, 0) for key in real.keys()}
    for key in er.keys():
        if er[key] < 0:
            neg += er[key]
        else:
            pos += er[key]
    return {'neg': neg, 'pos': pos}


def forecastOneWeek(dt):
    fore = dict(dt)
    fore[1] = 0
    for i in range(2, 53):
         if i-1 in dt.keys():
            fore[i] = dt[i - 1]
         else:
            fore[i] = 0

    return fore

def forecastTwoWeek(dt):
    fore = dict(dt)
    for i in range(1, 53):
        if i < 3:
            fore[i] = 0
        else:
            fore[i] = int((dt[i-1]+dt[i-2])/2)
    return fore


def statistics_of_province(year, MaSP):
    o = os.listdir('../data/o' + str(year))
    r = os.listdir('../data/r' + str(year))
    rs1 = {}
    for i, j in zip(o, r):
        dt1 = pd.read_csv('../data/o' + str(year) + '/' + str(i))
        dt2 = pd.read_csv('../data/r' + str(year) + '/' + str(j))
        dt = pd.merge(dt1, dt2, how="inner", on=['shop', 'doc'])
        if str(i) in 'o201801.csv':
            a = SaleProvinceWeek(dt, MaSP[2:], d)
            rs1 = merge_dicts(rs1, a)
        elif str(i) in ('o' + str(year) + '12.csv'):
            dt['date'] = pd.to_datetime(dt['date'])
            compare = str(year) + '-12-31'
            dt = dt.loc[dt['date'] < compare]
            a = SaleProvinceWeek(dt, MaSP, d)
            rs1 = merge_dicts(rs1, a)
        else:
            a = SaleProvinceWeek(dt, MaSP, d)
            rs1 = merge_dicts(rs1, a)
    return rs1


def statistics_of_shop(year, MaSP, MaShop):
    o = os.listdir('../data/o' + str(year))
    r = os.listdir('../data/r' + str(year))
    rs1 = {}
    for i, j in zip(o, r):
        dt1 = pd.read_csv('../data/o' + str(year) + '/' + str(i))
        dt2 = pd.read_csv('../data/r' + str(year) + '/' + str(j))
        dt = pd.merge(dt1, dt2, how="inner", on=['shop', 'doc'])
        if str(i) in 'o201801.csv':
            a = SaleShopWeek(dt, MaSP[2:], MaShop)
            rs1 = merge_dicts(rs1, a)
        elif str(i) in ('o' + str(year) + '12.csv'):
            dt['date'] = pd.to_datetime(dt['date'])
            compare = str(year) + '-12-31'
            dt = dt.loc[dt['date'] < compare]
            a = SaleShopWeek(dt, MaSP, MaShop)
            rs1 = merge_dicts(rs1, a)
        else:
            a = SaleShopWeek(dt, MaSP, MaShop)
            rs1 = merge_dicts(rs1, a)
    return rs1

real = statistics_of_shop(2018,'00271554',30290)
real = dict(sorted(real.items()))
print(real)


# real = statistics_of_province(2018, '00269765')
# real = dict(sorted(real.items()))
# print(real)
keys1 = list(real.keys())
values1 = list(real.values())
#
# print(forecastTwoWeek(real))

forecast = dict(sorted(forecastOneWeek(real).items()))
keys2 = list(forecast.keys())
values2 = list(forecast.values())
# print(forecast)
# forecast = dict(sorted(forecastTwoWeek(real).items()))
# keys2 = list(forecast.keys())
# values2 = list(forecast.values())

plt.subplots(figsize=(10, 4))
plt.plot(keys1, values1, '.-', label='real')

plt.plot(keys2, values2, '.-', label='forecast')

plt.xlabel('Week')
plt.ylabel('Revenue of Hanoi')
plt.savefig('forest.png')
plt.legend(['real', 'forecast'], loc=4)
plt.show()


print(error(forecast, real))