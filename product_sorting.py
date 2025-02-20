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
df_ = pd.read_json('Dataset/Digital_Music.jsonl', lines=True)
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

# Rating Distribution
df['rating'].value_counts()
df.head()

########################################################################
# AVERAGE
# Ürünlere göre rating sayıları
product_ratings = df.groupby('asin').agg({'rating':'mean'}).reset_index()

product_ratings.rename(columns={'rating': 'average_rating'}, inplace=True)
df = pd.merge(df,product_ratings, how='left', on='asin')
df.head(10).sort_values('average_rating', ascending=False)



# Puan dağılımını görselleştirmek
plt.figure(figsize=(10, 5))
sns.histplot(df["rating"], bins=5, kde=True)
plt.xlabel("Product Rating")
plt.ylabel("Comment Count")
plt.title("Product Rating Distribution")
plt.show()

########################################################################
## Ağırlıklı ortalama hesaplama (helpful_vote)
## daha fazla faydalı oy almış yorumlara daha fazla ağırlık verebilirsin:

# Ağırlıklı ortalama: (rating * helpful_vote) toplamının helpful_vote toplamına bölümü
df["helpful_vote_scaled"] = MinMaxScaler(feature_range=(1 ,5)).fit(df[["helpful_vote"]]).transform(df[["helpful_vote"]])
df['weighted_rating'] = df['rating'] * df['helpful_vote_scaled']

weighted_averaged_rating = df.groupby('asin').agg({'weighted_rating':'mean'}).reset_index()
weighted_averaged_rating.rename(columns={'weighted_rating': 'weighted_average_rating'}, inplace=True)
df = pd.merge(df,weighted_averaged_rating, how='left', on='asin')
df.sort_values('weighted_average_rating', ascending=False)



########################################################################

# Time-Based Weighted Average (Puan Zamanlarına Göre Ağırlıklı Ortalama)
df['timestamp'].max()
df['timestamp'].min()
current_time = dt.datetime(2023,9,8)
df['days_diff'] = (current_time - df['timestamp']).dt.days

df[df['days_diff'] < 30].head()

def time_based_weighted_rating(product, w1=40, w2=30, w3=20, w4=10):

    return product.loc[product['days_diff'] <= product['days_diff'].quantile(0.25), 'rating'].mean() * w1/100 + \
    product.loc[(product['days_diff'] > product['days_diff'].quantile(0.25))& (product['days_diff'] <=product['days_diff'].quantile(0.5)), 'rating'].mean() * w2/100 + \
    product.loc[(product['days_diff'] > product['days_diff'].quantile(0.5))& (product['days_diff'] <=product['days_diff'].quantile(0.75)), 'rating'].mean() * w3/100 + \
    product.loc[(product['days_diff'] > product['days_diff'].quantile(0.75)), 'rating'].mean() * w4/100


df_time_rating = df[['asin','rating', 'days_diff']]
df_time_rating['days_diff'].describe()

time_based_weighted_rating_score = df_time_rating.groupby('asin').apply(time_based_weighted_rating).dropna()
time_based_weighted_rating_score = time_based_weighted_rating_score.reset_index()

time_based_weighted_rating_score.columns = ['asin','tbwr_score']
df = pd.merge(df, time_based_weighted_rating_score, how='left', on='asin')
df.sort_values('tbwr_score', ascending=False).head(20)



########################################################################

# User-Based(Quality) Weighted Average (Kullanıcı Temelli Ağırlıklı Ortalama)
df = df_.copy()
user_review_counts = df.groupby('user_id').size().reset_index(name='total_review_count')
user_review_counts.sort_values('total_review_count', ascending=False)
df = pd.merge(df, user_review_counts, on='user_id', how='left')

average_helpful_vote = df.groupby('user_id').agg({'helpful_vote':'mean'}).reset_index()
average_helpful_vote.columns = ['user_id', 'average_helpful_vote']
df = pd.merge(df, average_helpful_vote, on='user_id', how='left')

df.sort_values('average_helpful_vote', ascending=False)

# df["helpful_vote_scaled"] = MinMaxScaler(feature_range=(1 ,5)).fit(df[["helpful_vote"]]).transform(df[["helpful_vote"]])
# df['weighted_rating'] = df['rating'] * df['helpful_vote_scaled']

df['user_trust_score'] = (df["helpful_vote_scaled"] * 0.7 )+ (df["weighted_rating"] * 0.3)

# Kullanıcının toplam yorum sayısını 1-5 aralığına ölçeklendir
df["total_review_count_scaled"] = MinMaxScaler(feature_range=(1, 5)).fit_transform(df[["total_review_count"]])

# Kullanıcı güven skoru (user_trust_score) ve yorum sayısını ağırlıklı şekilde birleştir
df["final_weighted_score"] = (df["user_trust_score"] * 0.6) + (df["total_review_count_scaled"] * 0.4)

# Ürün bazında ağırlıklı ortalama puanı hesapla
product_weighted_avg_score = df.groupby("asin").agg({"final_weighted_score": "mean"}).reset_index()
product_weighted_avg_score.columns = ['asin','final_weighted_average_score']
df = pd.merge(df, product_weighted_avg_score, how='left', on='asin')
columns = ['rating','title','asin','user_id','final_weighted_average_score']

df[columns].sort_values(by='final_weighted_average_score', ascending=False)
df.columns
