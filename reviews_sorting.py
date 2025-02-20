import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from sklearn.preprocessing import MinMaxScaler



pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Reading the csv file
df_ = pd.read_json('datasets/Digital_Music.jsonl', lines=True)
# Some large JSON files may be line-delimited JSON. In such a case you should use the lines=True parameter
df = df_.copy()
df.info()
# Let's select the variables we will use and reassign them to df.
df = df[['rating','title','asin','user_id','timestamp','helpful_vote','verified_purchase']]
df = df[df['timestamp'] > '2018-01-01']
# Let's Analyze the Data Set
def check_data(dataframe):
    print("########################## HEAD ##########################")
    print(dataframe.head())
    print("########################## INFO ##########################")
    print(dataframe.info())
    print("########################## SHAPE ##########################")
    print(dataframe.shape)
    print("########################## ISNULL(?) ##########################")
    print(dataframe.isnull().sum())
    print("########################## DESCRIBE ##########################")
    print(dataframe.describe().T)
    print("####################################################")

check_data(df)


# Zaman'a ve Faydalı Bulunma Sayılarına Göre Ürün Yorum Sıralama
df_product =df[df['asin']=='B00003CXKT']
drop_list=['title','text', 'images','parent_asin', 'user_id', 'verified_purchase']
df_product.drop(drop_list, axis=1, inplace=True)
df_product.sort_values('helpful_vote', ascending=False)
df_product['helpful_vote_scaled'] = MinMaxScaler(feature_range=(1, 5)).fit(df_product[['helpful_vote']]).transform(df_product[['helpful_vote']])

df_product['timestamp'].max() # '2003-06-20 20:00:13'
df_product.sort_values('timestamp', ascending=False)
current_time = dt.datetime(2003,6,22)
df_product['days_diff'] = (current_time - df_product['timestamp']).dt.days
df_product['days_diff_scaled'] = MinMaxScaler(feature_range=(1, 5)).fit_transform(df_product[['days_diff']])

df_product.sort_values('rating', ascending=False)
df_product.info()

def weighted_review_sorting_score(product, w1=33,w2=30,w3=37):
    return product['helpful_vote_scaled'] * w1/100 + \
        product['days_diff_scaled'] * w2/100 + \
        product['rating'] * w3/100


df_product['wrs'] = weighted_review_sorting_score(df_product)

df_product.sort_values('wrs', ascending=False).head(10)
