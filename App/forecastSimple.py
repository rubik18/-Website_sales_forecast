import os
import pandas as pd
import matplotlib.pyplot as plt



def SaleShopWeek(data, MaSP, MaShop):
    data['date'] = pd.to_datetime(data['date'])
    data['week'] = data['date'].apply(lambda x: x.isocalendar()[1])
    result = data[(data['shop'] == MaShop) & (data['item'] == str(MaSP)) & (data["status"] == "F") & (data['qty'] <= 3)]
    # print(result)
    nameSp = list(result['desc'])
    arr = list(result['week'])
    dic = {}
    for x in arr:
        re = result[result['week']== x]
        dic[x] = sum(re['qty'])
    return dic, nameSp

def SaleProvinceWeek(data, MaSP, ListShop):
    data['date'] = pd.to_datetime(data['date'])
    data['week'] = data['date'].apply(lambda x: x.isocalendar()[1])
    result = data[(data['shop'].isin(ListShop)) & (data['item'] == str(MaSP)) & (data["status"] == "F") & (data['qty'] <= 3)]
    # print(result)
    nameSp = list(result['desc'])
    arr = list(result['week'])
    dic = {}
    for x in arr:
        re = result[result['week'] == x]
        dic[x] = sum(re['qty'])
    return dic,nameSp

def merge_dicts(dict1, dict2):
    for k, v in dict2.items():
        if k in dict1:
            dict1[k] += v
        else:
            dict1[k] = v
    return dict1

def statistics_of_province(year, MaSP,listShop):
    o = os.listdir('../data/o' + str(year))
    r = os.listdir('../data/r' + str(year))
    rs1 = {}
    name=[]
    for i, j in zip(o, r):
        dt1 = pd.read_csv('../data/o' + str(year) + '/' + str(i))
        dt2 = pd.read_csv('../data/r' + str(year) + '/' + str(j))
        dt = pd.merge(dt1, dt2, how="inner", on=['shop', 'doc'])
        a,nam = SaleProvinceWeek(dt, MaSP, listShop)
        if nam :
            name=nam
        rs1 = merge_dicts(rs1, a)
    return sorted(rs1.items(), key=lambda x: x[0]),name[0]


def statistics_of_shop(year, MaSP, MaShop):
    o = os.listdir('../data/o' + str(year))
    r = os.listdir('../data/r' + str(year))
    rs1 = {}
    name=[]
    for i, j in zip(o, r):
        dt1 = pd.read_csv('../data/o' + str(year) + '/' + str(i))
        dt2 = pd.read_csv('../data/r' + str(year) + '/' + str(j))
        dt = pd.merge(dt1, dt2, how="inner", on=['shop', 'doc'])
        a , nam = SaleShopWeek(dt, MaSP, MaShop)
        if nam :
            name=nam
        rs1 = merge_dicts(rs1, a)
    return sorted(rs1.items(), key=lambda x: x[0]),name[0]
    # print(name[0])
def error(forecast, real):
    neg, pos = 0, 0
    er = {key: real[key] - forecast.get(key, 0) for key in real.keys()}
    for key in er.keys():
        if er[key] < 0:
            neg += er[key]
        else:
            pos += er[key]
    return neg, pos


def forecastOneWeek(dt):
    fore = dict(dt)
    fore[1] = 0
    for i in range(2, 53):
         if i-1 in dt.keys():
            fore[i] = dt[i - 1]
         # else:
         #    fore[i] = 0
    neg,pos = error(fore,dt)
    return fore,neg,pos

def forecastTwoWeek(dt):
    fore = dict(dt)
    for i in range(1, 53):
        if i < 3:
            fore[i] = 0
        else:
            fore[i] = int((dt[i-1]+dt[i-2])/2)
    neg, pos = error(fore, dt)
    return fore, neg, pos

def name( MaShop):
    listShop = pd.read_csv("../data/fptshop.csv")
    shop = list(listShop[listShop["Code"]==MaShop]["Name"])
    return shop[0]

# forecastOneWeek in shop
def main1(id,shop):
    #  iPhone 6s Plus 32GB Gold (A1687)
    # real = statistics_of_shop(2018,'00271554',30290)
    real, name = statistics_of_shop(2018,str(id),shop)
    print(name)
    real = dict(real)
    print(real)
    fore, neg,pos = forecastOneWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg,",",pos)
    x1 = list(real.keys())
    y1 = list(real.values())

    x2 = list(fore.keys())
    y2 = list(fore.values())

    plt.subplots(figsize=(9, 4))
    p1, = plt.plot(x1,y1,'b.-')
    p2, = plt.plot(x2,y2,'r.-')
    plt.title('iPhone 6s Plus 32GB Gold (A1687) tại shop HNI 61 Trần Duy Hưng(A)')
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1,p2], ["real", "forcast_1week"])
    imgName = 'static/img/'+str(id) + str(shop) + '.png'
    plt.savefig(imgName)
    plt.show()
##### forecastOneweek in provinces
def main2(id,provinces):
    listShop = pd.read_csv("../data/fptshop.csv")
    d = list(listShop[listShop["Provinces"] == str(provinces)]["Code"])
    real = statistics_of_province(2018, str(id),d)
    real = dict(real)
    # print(real)
    fore, neg, pos = forecastOneWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg, ",", pos)
    x1 = list(real.keys())
    y1 = list(real.values())

    x2 = list(fore.keys())
    y2 = list(fore.values())

    plt.subplots(figsize=(9, 4))
    p1, = plt.plot(x1, y1, 'b.-')
    p2, = plt.plot(x2, y2, 'r.-')
    plt.title('iPhone 6s Plus 32GB Gold (A1687) tại Hà Nội')
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1, p2], ["real", "forcast_2week"])
    imgName = 'static/img/'+ (id) + str(provinces) + '.png'
    plt.savefig(imgName)
    plt.show()

if __name__ == '__main__':
    # name
    # a,b = statistics_of_shop(2018,'00271554',30290)
    # print(a)
    # print(b)
    a = [(1, 2), (2, 2), (3, 1), (4, 2), (5, 4), (6, 6), (7, 1), (8, 4), (9, 7), (10, 8), (11, 4), (12, 1), (13, 4),(14, 4), (15, 1), (16, 1), (17, 2), (18, 2), (20, 1), (21, 1), (22, 2), (25, 1), (26, 1), (27, 6), (28, 2),(29, 1), (31, 1), (32, 1), (33, 1), (34, 4), (36, 1), (37, 2), (38, 1), (39, 1), (43, 1), (45, 2), (46, 2),(47, 2), (48, 2), (50, 2), (51, 2), (52, 3)]
    # a=  [(1, 1), (2, 1), (4, 1), (7, 1), (9, 1), (10, 4), (11, 1), (12, 2), (19, 1), (27, 1), (32, 1), (39, 1), (40, 1), (41, 1), (45, 1), (46, 1), (48, 1), (50, 3), (51, 1)]
    # print(a)
    # a.append((53,0))
    # for i in range(0,52):
    #     print('i=',i,'a[i][0]=',a[i][0])
    #     # print(a)
    #     if  a[i][0] != i+1 :
    #         x = (i+1,0)
    #         a.insert(i,x)
    # print(a)
    # a.pop(52)
    # # print(type(a))
    #
    #
    # print(a)

    print(name(30290))
    # main1('00336612',30290)
    # main2('00271554',"Hà Nội")
    # a = {1: 0, 2: 82, 3: 52, 4: 76, 5: 98, 6: 145, 7: 201, 8: 110, 9: 124, 10: 158, 11: 223, 12: 130, 13: 69, 14: 69, 15: 65, 16: 72, 17: 54, 18: 74, 19: 49, 20: 43, 21: 58, 22: 60, 23: 60, 24: 43, 25: 45, 26: 55, 27: 51, 28: 59, 29: 54, 30: 50, 31: 59, 32: 50, 33: 58, 34: 47, 35: 50, 36: 38, 37: 49, 38: 45, 39: 45, 40: 38, 41: 54, 42: 50, 43: 68, 44: 60, 45: 59, 46: 51, 47: 56, 48: 65, 49: 57, 50: 87, 51: 59, 52: 55}





