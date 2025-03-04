from K_Means import KM_data


kmeans_analysis = KM_data[['R','F','M','类别']]

aaa = kmeans_analysis.groupby(['类别'])[['R','F','M',]].mean()

#重命名列
print(aaa)
print(KM_data.groupby(['类别'])[['R','F','M',]].mean())
print(KM_data.groupby(KM_data['类别'])[['R','F','M',]].mean())
