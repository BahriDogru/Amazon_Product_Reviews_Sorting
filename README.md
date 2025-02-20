# Amazon Ürün ve Yorum Sıralama

E-ticaret sitelerindeki ürünlerin sıralanması, birçok faktörün etkisiyle şekillenir. Ürünlerin derecelendirilmesinde kullanılan yöntemlerin temel amacı, müşterilerin veya kullanıcıların en doğru ürün veya hizmete ulaşmasını sağlamaktır.

Bir ürünün yüksek puan alması, o ürünün gerçekten kaliteli olduğunu garanti etmez. Kullanıcı yorumlarının tarafsızlığı ve puanlama sistemlerinin adilliği gibi konular, doğru ölçüm yöntemlerinin önemini vurgular. Kullanıcı puanlarının güvenilirliği, yorumların sıralanma biçimi ve verilerin işlenme yöntemleri, yanlış kararlara yol açabilir.

Bu proje, ürünlerin ve ürünlere yapılan yorumların analiz edilerek en güvenilir ve faydalı sıralamayı oluşturmayı amaçlar. Yorumları hem ürün bazında hem de genel kullanıcı güvenilirliği temelinde değerlendirerek daha doğru sıralamalar elde edilir.

## Kullanılan Yöntemler

1.  **Ürün Bazında Sıralama**

    *   Ürünlerin kullanıcıların verdiği puanlara göre sıralanması
    *   Ürünlerin aldığı yorum sayısı ve satın alınma durumlarına göre sıralanması
    *   Ürünlerin faydalı yorumlara ve satın alınma sayılarına göre sıralanması

2.  **Yorum Bazında Sıralama**

    *   Yorumların faydalı bulunup bulunulmadığı ve zaman'a göre en yeni ve en eski yorumların ağırlıklarına göre sıralama

## Kullanılan Kütüphaneler

*   Pandas
*   NumPy
*   Matplotlib
*   Scikit-learn (MinMaxScaler)
*   Seaborn
*   Datetime

## Veri Seti

Bu projede Amazon Digital Music veri seti kullanılmıştır. Veri setine aşağıdaki adresten ulaşabilirsiniz:

 [Amazon Digital Music Veri Seti](https://jmcauley.ucsd.edu/data/amazon/)


 ********************************************************************************************************************************

 # Amazon Product and Review Sorting

The ranking of products on an e-commerce site is influenced by multiple factors. The goal of product ranking methods is to ensure that customers and users find the most relevant product or service.

Does a high product rating necessarily indicate high quality? Are user reviews unbiased? Are scoring systems always fair? These questions highlight the need for accurate measurement methods.  The reliability of user ratings, how reviews are ranked, and data processing methods can all lead to incorrect conclusions.

This project aims to create the most reliable and useful product ranking by analyzing both the products themselves and the reviews they receive.  By evaluating reviews on both a per-product basis and a general user reliability basis, we aim to achieve more accurate rankings.

## Methods Used

1.  **Product-Based Ranking**

    *   Ranking products by user ratings.
    *   Ranking products by the number of reviews and purchases.
    *   Ranking products by helpful reviews and the number of purchases.

2.  **Comment-Based Ranking**

    *   Ranking comments based on their helpfulness and recency, weighting newer and older comments differently.

## Libraries Used

*   Pandas
*   NumPy
*   Matplotlib
*   Scikit-learn (MinMaxScaler)
*   Seaborn
*   Datetime

## Dataset

This project uses the Amazon Digital Music dataset.  You can access the dataset at the following link:

[Amazon Digital Music Dataset](https://jmcauley.ucsd.edu/data/amazon/)
