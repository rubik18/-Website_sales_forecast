import pandas as pd
# from numpy.ma import column_stack
def zipData():
    df1 = pd.read_csv('../data/r2019/r201901.csv')
    for i in range(2, 10):
        df = pd.read_csv('../data/r2019/r20190' + str(i) + '.csv')
        df1 = df1.append(df)
    for i in range(10, 13):
        df = pd.read_csv('../data/r2019/r2019' + str(i) + '.csv')
        df1 = df1.append(df)
    return df1

d=pd.read_csv('../data/r2019/r201901.csv')
df2 = pd.read_csv('../data/o2019/o201901.csv')
Shop = pd.read_csv('../data/fptshop.csv')
def listShop(region):
    HaNoi = Shop[(Shop['Provinces'] == region) & (Shop['ShopType'] == 'A')].reset_index()
    LS = list(HaNoi['Code'])
    return LS
def top_sales_shop(data,i,maShop):
    data = data[(data['price'] > 0) & (data['qty'] <= 3) & (data['shop'] == maShop)]
    # print(data.head(20))
    data['amount'] = data['price'] * data['qty']
    # print(data.head(20))
    # value2 = data.groupby(['desc']).agg({'qty': 'sum', 'amount': 'sum'}).sort_values('amount', ascending=False).head()
    value = data.groupby(['item'] ).agg({'qty': 'sum', 'amount': 'sum'}).sort_values('amount', ascending=False).head(i)
    # value = value.drop(columns = ['qty', 'amount'])
    value['amount'] = value['amount'] .round(4)
    # return value.to_csv(r'../data/sale.csv')
    listName=[]
    num = []
    k = 1
    for i in value['qty'].keys():
        result = data[(data['item'] == i)]
        li=list(result['desc'])
        a=li[0]
        listName.append(a)
        num.append(k)
        k = k+1
    m = list(zip(num,value['qty'].keys(),listName, value['qty'].values, value['amount'].values))
    return m
def top_sales(data,i):
    data = data[(data['price'] > 0) & (data['qty'] <= 3)]
    # print(data.head(20))
    data['amount'] = data['price'] * data['qty']
    # print(data.head(20))
    # value2 = data.groupby(['desc']).agg({'qty': 'sum', 'amount': 'sum'}).sort_values('amount', ascending=False).head()
    value = data.groupby(['item'] ).agg({'qty': 'sum', 'amount': 'sum'}).sort_values('amount', ascending=False).head(i)
    # value = value.drop(columns = ['qty', 'amount'])
    # print(value)
    value['amount'] = value['amount'].round(4)
    # return value.to_csv(r'../data/sale.csv')
    listName = []
    num = []
    k=1
    for j in value['qty'].keys():
        result = data[(data['item'] == j)]
        li = list(result['desc'])
        a = li[0]
        listName.append(a)
        num.append(k)
        k=k+1
    m = list(zip(num,value['qty'].keys(), listName, value['qty'].values, value['amount'].values))
    return m
# print(top_sales(df1))

def top_sales_Region(data,i,region):
    LS = listShop(region)
    data = data[(data['price'] > 0) & (data['qty'] <= 3) & (data['shop'].isin(LS))]
    # print(data)
    data['amount'] = data['price'] * data['qty']
    value = data.groupby(['item']).agg({'qty': 'sum', 'amount': 'sum'}).sort_values('amount', ascending=False).head(i)
    # print(value)
    value['amount'] = value['amount'].round(4)
    listName = []
    num =[]
    k=1
    for i in value['qty'].keys():
        result = data[(data['item'] == i)]
        li = list(result['desc'])
        a = li[0]
        listName.append(a)
        num.append(k)
        k = k +1
    m = list(zip(num,value['qty'].keys(), listName, value['qty'].values, value['amount'].values))
    return m
    # return value.to_csv(r'../data/saleHaNoi.csv')
# print(top_sales_HaNoi(df1))

def top_sales_day_of_month_HaNoi(data1, data2):
    data1 = data1[(data1['price'] > 0) & (data1['qty'] < 5) & (data1['shop'].isin(LS))]
    # print(df1)
    temp = pd.merge(data1, data2, how='inner', on=['shop', 'doc'])
    data1 = data1.drop(columns=['doc', 'disc', 'desc', 'shop'])
    data2 = data2.drop(columns='amount')
    temp['amount'] = temp['price'] * temp['qty']
    temp['date'] = pd.to_datetime(temp['date'])
    temp['date_month'] = temp['date'].dt.strftime('%Y%m%d')
    res = temp[['date', 'date_month']].head()
    value = temp.groupby(['date_month']).agg({'amount': 'sum'})
    return value
    # return value.to_csv(r'../data/month.csv')
# print(top_sales_day_of_month(df1, df2))

def top_sales_week_Provinces(data1, data2):
    data1 = data1[(data1['price'] > 0) & (data1['qty'] < 5) & (data1['shop'].isin(LS))]
    # print(df1)
    temp = pd.merge(data1, data2, how='inner', on=['shop', 'doc'])
    data1 = data1.drop(columns=['doc', 'disc', 'desc', 'shop'])
    data2 = data2.drop(columns='amount')
    temp['amount'] = temp['price'] * temp['qty']
    temp['date'] = pd.to_datetime(temp['date'])
    temp['week'] = temp['date'].apply(lambda x: x.isocalendar()[1])
    # print(temp)
    value = temp.groupby(['week']).agg({'amount': 'sum'})
    return value
    # return value.to_csv(r'../data/weekHaNoi.csv')
# print(top_sales_week_Provinces(df1, df2))

def top_sales_week(data1, data2):
    data1 = data1[(data1['price'] > 0) & (data1['qty'] < 5)]
    data2 = data2.drop(columns='amount')
    temp = pd.merge(data1, data2, how='inner', on=['shop', 'doc'])
    temp['amount'] = temp['qty'] * temp['price']
    temp['date'] = pd.to_datetime(temp['date'])
    temp['week'] = temp['date'].apply(lambda x: x.isocalendar()[1])
    value = temp.groupby(['week']).agg({'amount': 'sum'})
    # return value.to_csv(r'../data/week.csv')
    return value
# print(top_sales_week(df1, df2))

# print('Dữ liệu được lấy từ tháng 1 năm 2019')
# print('--------------------------------------')
# print('Top doanh thu trên cả nước')
if __name__ == '__main__':
    # a=top_sales_Region(d,10,'Hà Nội')
    # print(a)
    b = top_sales_shop(d,10,30290)
    print(b)
    # data = zipData()
    # c = top_sales(data, 10)
    # c = top_sales(d,10)
    # print(c)
    # for i in range(0,len(c)):
    #     print(i+1,c[i][0],c[i][1],c[i][2],c[i][3])


# print('--------------------------------------')
# print('Top doanh thu các shop hạng A trên địa bàn Hà Nội')
# print(top_sales_HaNoi(df1,20))
# print('--------------------------------------')
# print('Doanh thu từng ngày trong tháng')
# a=top_sales_day_of_month_HaNoi(df1, df2)
# m=dict(zip(a['amount'].keys(),a['amount'].values))

# print('--------------------------------------')
# print('Doanh thu theo tuần các shop hạng A trên địa bàn Hà Nội')
# b=top_sales_week_Provinces(df1, df2)
# print(type(b))
# print('--------------------------------------')
# print('Doanh thu theo tuần trên cả nước')
# c=top_sales_week(df1, df2)
# print(type(c))