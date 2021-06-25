
from flask import Flask, render_template
from flask import request
import matplotlib.pyplot as plt
import pandas as pd
import forecastSimple
import topSales

app = Flask(__name__)

@app.route('/')
def showApp():
   return render_template("base.html",methodd='"Một tuần"',name1 = "iphone 6S Plus 32G Gold (A1687)", name2 = "Hà Nội" ,neg = 462,pos=529,
                          posts={1: 0, 2: 82, 3: 52, 4: 76, 5: 98, 6: 145, 7: 201, 8: 110, 9: 124, 10: 158, 11: 223, 12: 130, 13: 69, 14: 69, 15: 65, 16: 72, 17: 54, 18: 74, 19: 49, 20: 43, 21: 58, 22: 60, 23: 60, 24: 43, 25: 45, 26: 55, 27: 51, 28: 59, 29: 54, 30: 50, 31: 59, 32: 50, 33: 58, 34: 47, 35: 50, 36: 38, 37: 49, 38: 45, 39: 45, 40: 38, 41: 54, 42: 50, 43: 68, 44: 60, 45: 59, 46: 51, 47: 56, 48: 65, 49: 57, 50: 87, 51: 59, 52: 55},
                          fileImg='/static/img/00271554HaNoi.png')

@app.route('/topShop',methods=['POST'])
def topShop():
    qty = request.form['qty']
    id_shop = request.form['id_shop']
    print(qty, type(qty), id_shop, type(id_shop))
    print(int(qty), int(id_shop))
    shop=' tại cửa hàng ' + forecastSimple.name(int(id_shop))
    # d = pd.read_csv('../data/r2019/r201901.csv')
    data = topSales.zipData()
    re = topSales.top_sales_shop(data,int(qty),int(id_shop))
    return render_template("statistic.html",qty=qty,type=shop,list=re)


@app.route('/topRegion',methods=['POST'])
def topRegion():
    qty = request.form['qty']
    id_region = request.form['id_region']
    print(qty,  id_region)
    shop = ' tại ' + str(id_region)
    # d = pd.read_csv('../data/r2019/r201901.csv')
    data = topSales.zipData()
    re = topSales.top_sales_Region(data,int(qty),str(id_region))
    return render_template("statistic.html", qty=qty, type=shop, list=re)

@app.route('/topAll',methods=['POST'])
def topAll():
    qty = request.form['qty']
    print(qty)
    shop = ' trên toàn hệ thống '
    # d = pd.read_csv('../data/r2019/r201901.csv')
    data = topSales.zipData()
    re = topSales.top_sales(data, int(qty))
    return render_template("statistic.html", qty=qty, type=shop, list=re)

@app.route('/forcast1_shop',methods=['POST'])
def forcast1_shop():
    id_item = request.form['id_item']
    id_shop = request.form['id_shop']
    print(str(id_item),"&&&", id_shop)
    shop = 'cửa hàng '+ forecastSimple.name(int(id_shop))
    real, sp = forecastSimple.statistics_of_shop(2018, str(id_item), int(id_shop))
    name = sp + ' tại '+ shop
    real.append((53,0))
    for i in range(0, 52):
        if real[i][0] != i + 1:
            x = (i + 1, 0)
            real.insert(i, x)
    real.pop(52)
    real = dict(real)
    # print(real)

    fore, neg, pos = forecastSimple.forecastOneWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg, ",", pos)
    x1 = list(real.keys())
    y1 = list(real.values())
    x2 = list(fore.keys())
    y2 = list(fore.values())
    plt.subplots(figsize=(10, 4))
    p1, = plt.plot(x1, y1, 'b.-')
    p2, = plt.plot(x2, y2, 'r.-')
    plt.title(name)
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1, p2], ["real", "forcast_1week"])
    imgName = '/static/img/' + str(id_item) + str(id_shop) + '.png'
    imgName2 = 'static/img/' + str(id_item) + str(id_shop) + '.png'
    print(imgName)
    plt.savefig(imgName2)
    plt.show()
    return render_template("forcast1_shop.html",methodd='"Một tuần"',neg=neg,pos=pos,sp=sp,shop=shop,
                           posts=fore,
                           fileImg=imgName)


@app.route('/forcast1_Region',methods=['POST'])
def forcast1_Region():
    id_item = request.form['id_item']
    id_region = request.form['id_region']
    listShop = pd.read_csv("../data/fptshop.csv")
    d = list(listShop[listShop["Provinces"] == id_region]["Code"])
    print(str(id_item), "&&&", id_region)
    real, sp = forecastSimple.statistics_of_province(2018, str(id_item), d)
    name = sp + ' tại ' + id_region
    real.append((53,0))
    for i in range(0, 52):
        if real[i][0] != i + 1:
            x = (i + 1, 0)
            real.insert(i, x)
    real.pop(52)
    real = dict(real)
    # print(real)

    fore, neg, pos = forecastSimple.forecastOneWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg, ",", pos)
    x1 = list(real.keys())
    y1 = list(real.values())
    x2 = list(fore.keys())
    y2 = list(fore.values())
    plt.subplots(figsize=(10, 4))
    p1, = plt.plot(x1, y1, 'b.-')
    p2, = plt.plot(x2, y2, 'r.-')
    plt.title(name)
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1, p2], ["real", "forcast_1week"])
    imgName = '/static/img/' + str(id_item) + str(id_region) + '.png'
    imgName2 = 'static/img/' + str(id_item) + str(id_region) + '.png'
    print(imgName)
    plt.savefig(imgName2)
    plt.show()
    return render_template("forcast1_shop.html",methodd='"Một tuần"',neg=-neg,pos=pos,sp=sp,shop=id_region,
                           posts=fore,
                           fileImg=imgName)

# @app.route('/forcast1_all',methods=['POST'])
# def forcast1_all():
#     id_item = request.form['id_item']
#

@app.route('/forecast2_shop',methods=['POST'])
def forecast2_shop():
    id_item = request.form['id_item']
    id_shop = request.form['id_shop']
    print(str(id_item), "&&&", id_shop)
    shop = 'cửa hàng ' + forecastSimple.name(int(id_shop))
    real, sp = forecastSimple.statistics_of_shop(2018, str(id_item), int(id_shop))
    print("real: ",real)
    name = sp + ' tại ' + shop
    real.append((53,0))
    for i in range(0, 52):
        if real[i][0] != i + 1:
            x = (i + 1, 0)
            real.insert(i, x)
    real.pop(52)
    real = dict(real)
    print(real)

    fore, neg, pos = forecastSimple.forecastTwoWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg, ",", pos)
    x1 = list(real.keys())
    y1 = list(real.values())
    x2 = list(fore.keys())
    y2 = list(fore.values())
    plt.subplots(figsize=(10, 4))
    p1, = plt.plot(x1, y1, 'b.-')
    p2, = plt.plot(x2, y2, 'r.-')
    plt.title(name)
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1, p2], ["real", "forcast_2week"])
    imgName = '/static/img/' + str(id_item) + str(id_shop) + 'w2.png'
    imgName2 = 'static/img/' + str(id_item) + str(id_shop) + 'w2.png'
    print(imgName)
    plt.savefig(imgName2)
    plt.show()
    return render_template("forcast1_shop.html",methodd = 'Trung bình trượt (Moving Average)', neg=neg, pos=pos, sp=sp, shop=shop,
                           posts=fore,
                           fileImg=imgName)

@app.route('/forecast2_region',methods=['POST'])
def forecast2_region():
    id_item = request.form['id_item']
    id_region = request.form['id_region']
    listShop = pd.read_csv("../data/fptshop.csv")
    d = list(listShop[listShop["Provinces"] == id_region]["Code"])
    print(str(id_item), "&&&", id_region)
    real,sp = forecastSimple.statistics_of_province(2018, str(id_item), d)
    name = sp + ' tại ' + id_region
    real.append((53,0))
    for i in range(0,52):
        if  real[i][0] != i+1 :
            x = (i+1,0)
            real.insert(i,x)
    real.pop(52)
    real = dict(real)
    # print(real)
    fore, neg, pos = forecastSimple.forecastTwoWeek(real)
    fore = dict(sorted(fore.items()))
    print(fore)
    print(neg, ",", pos)
    x1 = list(real.keys())
    y1 = list(real.values())
    x2 = list(fore.keys())
    y2 = list(fore.values())
    plt.subplots(figsize=(10, 4))
    p1, = plt.plot(x1, y1, 'b.-')
    p2, = plt.plot(x2, y2, 'r.-')
    plt.title(name)
    plt.xlabel('Week')
    plt.ylabel('Sales ')
    plt.legend([p1, p2], ["real", "forcast_2week"])
    imgName = '/static/img/' + str(id_item) + str(id_region) + 'w2.png'
    imgName2 = 'static/img/' + str(id_item) + str(id_region) + 'w2.png'
    print(imgName)
    plt.savefig(imgName2)
    plt.show()
    return render_template("forcast1_shop.html",methodd = 'Trung bình trượt (Moving Average)', neg=-neg, pos=pos,sp=sp, shop=id_region,
                           posts=fore,
                           fileImg=imgName)

# @app.route('/forecast2_all',methods=['POST'])
# def forecast2_all():
#     id_item = request.form['id_item']
#     print(str(id_item))
#     return '''Result : {}'''.format(id_item)

if __name__ == "__main__":
  app.run()