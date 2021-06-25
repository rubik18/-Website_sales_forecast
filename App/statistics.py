import pandas as pd


def salesShop(data, MaSP):
    rs = data[data["item"] == str(MaSP)]
    # print(rs.head())
    arr = list(rs["shop"])
    # print(arr)
    return dict((x, arr.count(x)) for x in arr)



def ValueShop(data, MaShop):
    value = data[(data["shop"] == MaShop) & (data["status"] == "F")]
    return sum(value["amount"])


def ValueShopDate(data, MaShop, date1, date2):
    data['date'] = pd.to_datetime(data['date'])
    new_df = data.loc[(data['date'] >= date1) & (data['date'] <= date2)]
    value = new_df[(new_df["shop"] == MaShop) & (new_df["status"] == "F")]
    return sum(value["amount"])


data = pd.read_csv("../data/o2018/o201801.csv")
# print(a.head())
b = pd.read_csv("../data/r2018/r201801.csv")
# print(b.head())

c = pd.read_csv("../data/fptshop.csv")

# Doanh số bán hàng  tất cả các shop tại cả hà nội
d = list(c[c["Provinces"] == "Hà Nội"]["Code"])

TotalValue = sum([ValueShop(data, i) for i in d])

print("Doanh số của tất cả các shop tại Hà Nội là:", TotalValue)


date1 = '2018-01-03'
date2 = '2018-01-10'
MaShop = 31233
# Doanh số bán hàng tại một shop
print("Doanh số của shop " + str(MaShop) + " là:", ValueShop(data, 31233))
# Doanh so ban hang tai một shop từ date1 đến date2
print("Doanh số của shop từ " + date1 + " đến " + date2 + " của shop " + str(MaShop) + " là:", ValueShopDate(data, 31233, date1, date2))
print(salesShop( b, 271554))