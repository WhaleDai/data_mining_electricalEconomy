import pandas as pd
from datetime import datetime
from math import ceil

# 3读入数据
datafile = "./data/Analysis.xlsx"
data = pd.read_excel(datafile)

# 4数据探查，观察前10行数据
print(data.head(10))

# 4.2查看行列数统计
print(data.shape)   #(301, 12)

# 4.3查看数据整体描述信息
print(data.info())

# 4.4查看各列数据的汇总统计集合
print(data.describe())

# 5数据缺失值处理，统计数据缺失值
print(data.isnull().sum())

# 6检测和过滤异常值: 统计有0值的数据列;统计空字符串的数据列 print((data == ' ').any())
print((data == 0).any())

# 统计每一列0值数据的个数
# 遍历data的每一列
for col in data.columns:
    # count从0开始累加
    count = 0
    # 如果值为0，则count累加
    count = [count + 1 for x in data[col] if x == 0]
    # 输出该列的0值个数
    print(col + ' ' + str(sum(count)))


# 调出gender与age两列都为0值的行
index1 = (data['gender'] == 0 ) & (data['age'] == 0)
print(data[index1])

# 调出pay_num，pay_times两者有一项为0值的行
index2 = (data['pay_num'] == 0) | (data['pay_times'] == 0)
print(data[index2])

# 将以上两种情况结合在一起，将无效数据行调出来统计
index3 = (data['gender'] == 0 ) & (data['age'] == 0) | (data['pay_num'] == 0) | (data['pay_times'] == 0)
print(data[index3])     #[13 rows x 12 columns]

# 删除13条记录
data = data.drop(data[index3].index)
print(data.shape)       #(288, 12)

# 7处理重复值
# 统计重复值
print(data.duplicated().sum())              #0
# 统计user_id这一列的重复值
print(data.duplicated(['user_id']).sum())   #2

# 删除重复值
data = data.drop_duplicates(['user_id'])
print(data.shape)                           #(286, 12)

# 统计不同性别和不同年龄的人数
gender = pd.Series(data['gender']).value_counts()
age = pd.Series(data['age']).value_counts()
# print(gender, age)

# 8属性规约
data_select = data[['user_id','last_pay_time','pay_num','pay_times']]
print(data_select.head())
#重命名列名
data_select.columns = ['用户id','最后一次消费时间','消费金额','消费次数']
print(data_select.head())

# 9计算特征R, F, M
# 生成起始日期和提数日的日期
start_date = datetime(2016, 6, 1)
exdata_date = datetime(2016, 7, 20)    #提数日的日期
print(start_date,exdata_date)          #2016-06-01 00:00:00 2016-07-20 00:00:00     日期类型数据

# 计算R
# 转化为可计算的日期类型数据
data_select = data_select.copy()
data_select['最后一次消费时间'] = pd.to_datetime(data_select['最后一次消费时间'])
# 计算R（最后一次消费距离提数日的时间）
data_select = data_select.copy()
data_select['R(最后一次消费距提数提数日的时间)'] = exdata_date - data_select['最后一次消费时间']

# 计算F（月均消费次数）
# 计算最后一次消费时间与起始日期的天数差
period_day = data_select['最后一次消费时间'] - start_date
# 创建空列表统计月数
period_month = []
# 遍历天数，向上取整生成月数
for i in period_day:
    period_month.append(ceil(i.days/30))
# 第一次输出月数统计
print(period_month)
# 分割线
print("#"*110)
# 遍历清楚0值
for i in range(0, len(period_month)):
    if period_month[i] == 0:
        period_month[i] =1
# 第二次输出月数统计
print(period_month)
# 计算F（月均消费次数）
data_select = data_select.copy()
data_select['F(月均消费次数)'] = data_select['消费次数']/period_month

# 计算M（月均消费金额）
data_select = data_select.copy()
data_select['M(月均消费金额)'] = data_select['消费金额']/period_month
print(data_select)

# 10保存预处理完成的数据
# 去掉每个列标签字符串前后的空格
data_select = data_select.rename(columns=lambda  x:x.strip())
# 保存数据
output_file_path = './data/Customer_info.xlsx'
data_select.to_excel(output_file_path, index=False)
