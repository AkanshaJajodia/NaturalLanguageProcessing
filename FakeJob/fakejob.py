# -*- coding: utf-8 -*-
"""FakeJob.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zWcW7eM0LBL6AVomDTCjuup5I97Pklqo
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
sns.set_theme(style="whitegrid")
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

!ls "drive/MyDrive/Colab Notebooks/FakeJob"

datadir="drive/MyDrive/Colab Notebooks/FakeJob/"

df = pd.read_csv(f'{datadir}/fake_job_postings.csv')

df.head()

df.describe()

df.info()

df.isnull().sum()

df.location = df.location.fillna('blank')

df.location

df.location.isnull().sum()

df_us = df[df['location'].str.contains("US")]

df_us.shape

loc_split =[]
for loc in df_us.location:
    loc_split.append(loc.split(','))

loc_split = pd.DataFrame(loc_split)

loc_split = loc_split[[1, 2]]

loc_split = loc_split.rename(columns={1: "state", 2:'city'})

loc_split

len(df_us)/len(df)

df_us = df_us.reset_index()

df_us

df_us = df_us.join(loc_split)

df_us

df_us = df_us[['job_id', 'title', 'location', 'department', 'salary_range',
       'company_profile', 'description', 'requirements', 'benefits',
       'telecommuting', 'has_company_logo', 'has_questions', 'employment_type',
       'required_experience', 'required_education', 'industry', 'function',
       'fraudulent', 'state', 'city']]

df_us = df_us[df_us['city'].notna()]
df_us = df_us[df_us['state'].notna()]

df_us.shape

df_us['state_city'] = df_us['state'] + ", " + df_us['city']

df_us

df_us.isna().sum()

df_us.city = df_us.city.str.strip()
df_us.state = df_us.state.str.strip()
df_us.head(10)

corr = df_us.corr()
sns.heatmap(corr)
plt.show()

len(df_us[df_us.fraudulent == 0]), len(df_us[df_us.fraudulent == 1]),

sns.countplot(x='fraudulent', data=df_us);

def sns_countplot(feature):
    sns.countplot(x=feature, data=df_us, hue="fraudulent",
              order=df_us[feature].value_counts().iloc[:10].index)
    plt.xticks(rotation=45)
    title = feature + ' fake job count'
    plt.title('Location Fake Jobs')
    plt.show()

plt.figure(figsize=(10,10))
df_us.groupby('state').fraudulent.count().plot(kind='bar', title='Job count by states');

plt.figure(figsize=(10,6))
sns.countplot(x='state', data=df_us, hue="fraudulent", order=df_us['state'].value_counts().iloc[:10].index)
plt.xticks(rotation=45)
plt.show()

sns.countplot(x='state_city',
              data=df_us, hue="fraudulent", order=df_us['state_city'].value_counts().iloc[:10].index)
plt.xticks(rotation=45)
plt.show()

def sns_countplot(feature):
    sns.countplot(x=feature, data=df_us, hue="fraudulent",
              order=df_us[feature].value_counts().iloc[:10].index)
    plt.xticks(rotation=45)
    title = feature + ' fake job count'
    plt.title(title)
    plt.show()

sns_countplot('employment_type');

sns_countplot('required_education');

location_ratio = round(df_us[df_us.fraudulent == 1].groupby('state_city').state_city.count()/df_us[df_us.fraudulent == 0].groupby('state_city').state_city.count(), 2)
location_ratio = pd.DataFrame({'state_city':location_ratio.index, 'ratio':location_ratio.values})

location_ratio

df_us = df_us.merge(location_ratio)

df_us.ratio.fillna(0, inplace=True)

location_ratio_plot = location_ratio[location_ratio.ratio >= 1]

sns.barplot(data=location_ratio_plot.sort_values(by='ratio'), x='state_city', y='ratio')
plt.xticks(rotation=45)
plt.title('Fake to Real Job Ratio')
plt.show()

def missing_count(feature, title='None'):
    y_axis = df_us[df_us[feature].isna()][['fraudulent', feature]]
    y_axis = y_axis.fraudulent.value_counts()
    y_axis.plot(kind='bar')
    plt.ylabel('Count')
    plt.xlabel('Category')
    title = "Number of empty " + title + " in fraudulent and non-fraudulent"
    plt.title(title)
    plt.xticks(rotation=0)
    plt.show()
    return 0

missing_count('function', 'Functions')

missing_count('company_profile', 'Company Profile')

missing_count('required_education', 'required_education')

missing_count('industry', 'Industry')

missing_count('benefits', 'Benefits')

telecommuting_list = []
has_company_logo_list = []

for idx, tel, logo in zip(range(len(df_us)), df_us.telecommuting, df_us.has_company_logo):
    if df.fraudulent[idx] == 1:
        telecommuting_list.append(tel)
        has_company_logo_list.append(logo)
    else:
        pass

telecommuting_logo_df = pd.DataFrame({'telecommuting':telecommuting_list, 'has_company_logo':has_company_logo_list})

telecommuting_logo_df

fake_count = 0

for fraud, tel, logo in zip(df_us.fraudulent, df_us.telecommuting, df_us.has_company_logo):
    if (tel == 0 and logo == 0):
        if (fraud == 1):
            fake_count +=1
        else:
            pass
    else:
        pass


print(fake_count)

fake_count = 0

for fraud, tel, logo, ques in zip(df_us.fraudulent, df_us.telecommuting, df_us.has_company_logo, df_us.has_questions):
    if (tel == 0):# and logo == 0 and ques == 0):
        if (fraud == 1):
            fake_count +=1
      

print(fake_count)

len(df_us[df_us.fraudulent == 1])

fake_count/len(df_us[df_us.fraudulent == 1]) * 100

df_us.fillna(" ",inplace = True)

df_us['text'] =  df_us['title'] + ' ' + df_us['location'] + ' ' + df_us['company_profile'] + ' ' + \
        df_us['description'] + ' ' + df_us['requirements'] + ' ' + df_us['benefits'] + ' ' + \
        df_us['required_experience'] + ' ' + df_us['required_education'] + ' ' + df_us['industry'] + ' ' + df_us['function']


df_us.drop(['job_id', 'department', 'salary_range', 'title','location','department','company_profile','description','requirements','benefits','employment_type','required_experience','required_education','industry','function', 'city', 'state_city', 'has_company_logo', 'has_questions', 'state'], axis = 1, inplace = True)

df_us

df_us['character_count'] = df_us.text.apply(len)

df_us[df_us.fraudulent==0].character_count.plot(bins=35, kind='hist', color='blue', 
                                       label='Real', alpha=0.8)
df_us[df_us.fraudulent==1].character_count.plot(kind='hist', color='red', 
                                       label='Fake', alpha=0.8)
plt.legend()
plt.title('Frequency of Words')
plt.xlabel("Character Count");

df_us

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import nltk
nltk.download('punkt')

text = df_us.text.to_list()
text = ' '.join(text)
tokens_text = word_tokenize(text)

tokens_text

lower_tokens = [t.lower() for t in tokens_text]
word_freq = Counter(lower_tokens)
print(Counter.most_common(word_freq, 10))

text_only_alphabets = [t for t in lower_tokens if t.isalpha()]

nltk.download('stopwords')
english_stopped = stopwords.words('english')
no_stops = [t for t in text_only_alphabets if t not in english_stopped]

no_stops

nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()

lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
bow = Counter(lemmatized)
print(Counter.most_common(bow, 10))

df_us.to_csv(f'{datadir}/fake_job_postings_cleaned.csv')

!ls "drive/MyDrive/Colab Notebooks/FakeJob"

cleaned_df = pd.read_csv(f'{datadir}/fake_job_postings_cleaned.csv')

cleaned_df

X = cleaned_df[['telecommuting', 'ratio', 'text', 'character_count']]
y = cleaned_df['fraudulent']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=53)

X_train_num = X_train[['telecommuting', 'ratio', 'character_count']]
X_test_num = X_test[['telecommuting', 'ratio', 'character_count']]

count_vectorizer = CountVectorizer(stop_words='english')
count_train = count_vectorizer.fit_transform(X_train.text.values)
count_test = count_vectorizer.transform(X_test.text.values)

tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=1)
tfidf_train = tfidf_vectorizer.fit_transform(X_train.text)
tfidf_test = tfidf_vectorizer.transform(X_test.text)

count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())
tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())

count_df.head()

tfidf_df.head()

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split

nb_classifier = MultinomialNB()
nb_classifier.fit(count_train, y_train)
pred = nb_classifier.predict(count_test)
metrics.accuracy_score(y_test, pred)

metrics.f1_score(y_test, pred)

from sklearn.linear_model import SGDClassifier

clf_log = SGDClassifier(loss='log').fit(count_train, y_train)
pred_log = clf_log.predict(count_test)
metrics.accuracy_score(y_test, pred_log)

clf_num = SGDClassifier(loss='log').fit(X_train_num, y_train)
pred_num = clf_num.predict(X_test_num)
metrics.accuracy_score(y_test, pred_num)

prediction_array = []

for i, j in zip(pred_num, pred_log):
    if i == 0 and j == 0:
        prediction_array.append(0)
    else:
        prediction_array.append(1)

print("Accuracy:",metrics.accuracy_score(y_test, prediction_array))

print("F1_Score:",metrics.f1_score(y_test, prediction_array))

from sklearn.metrics import confusion_matrix

cf_matrix = confusion_matrix(y_test, prediction_array)

cf_matrix

group_names = ["True Negative","False Positive", "False Negative", "True Positive"]
group_counts = ["{0:0.0f}".format(value) for value in
                cf_matrix.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in
                      cf_matrix.flatten()/np.sum(cf_matrix)]
labels = [f'{v1}\n{v2}\n{v3}' for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues');

