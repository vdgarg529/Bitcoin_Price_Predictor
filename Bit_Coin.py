#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv("BTC.csv")


# In[3]:


df.tail(7)


# In[4]:


data=pd.DataFrame(df["Closing Price (USD)"])
data.rename(columns={'Closing Price (USD)':'Price'},inplace=True)


# In[5]:


data


# In[6]:


prediction_days=30
data['Prediction']=data[['Price']].shift(-prediction_days)


# In[7]:


data.head(30)


# In[8]:


data.tail(7)


# In[9]:


X = np.array(data.drop(['Prediction'],1))
X=X[:len(data)-prediction_days]
print(X)


# In[10]:


Y = np.array(data.drop(['Price'],1))
Y=Y[:len(data)-prediction_days]


# In[11]:


Y


# In[12]:


from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y, test_size=0.2)


# In[13]:


prediction_days_array=np.array(data.drop(['Prediction'],1))[-prediction_days:]


# In[14]:


from sklearn.svm import SVR
svr_rbf=SVR(kernel='rbf',C=1e3,gamma=0.0000001)
svr_rbf.fit(X_train,Y_train)


# In[15]:


svr_rbf_confidence=svr_rbf.score(X_test,Y_test)
svr_rbf_confidence


# In[16]:


svm_prediction=svr_rbf.predict(X_test)
a=pd.DataFrame(svm_prediction)
a['actual']=Y_test


# In[17]:


a.tail()


# In[18]:


svm_prediction_a=svr_rbf.predict(prediction_days_array)
b=pd.DataFrame(svm_prediction_a)
print(b)
print(data.tail(prediction_days))


# In[19]:


from pickle import dump
dump(svr_rbf,open("bitcoin_predictor.pkl","wb"))


# In[ ]:




