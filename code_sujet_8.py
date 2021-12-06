# -*- coding: utf-8 -*-
"""code -sujet-8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_hJJa7-zWjtcEqpjqOexB46mwyyJ7VrD
"""

import nltk 
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
#for saving the model
!pip install torch

import matplotlib.pyplot as plt
import os
import re
import shutil
import string

import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras import layers
from tensorflow.keras import losses
from collections import Counter

import pandas as pd
import numpy as np
    
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
    
from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pydot


import itertools
import nltk
from sklearn import model_selection

import matplotlib.pyplot as plt
import os
import re
import shutil
import string
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras import layers
from tensorflow.keras import losses
from collections import Counter
from nltk.stem import PorterStemmer
from nltk import pos_tag
porter = PorterStemmer()
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
    
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
    
from tensorflow.keras import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pydot

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam

import itertools
import nltk
from sklearn import model_selection
from nltk.corpus import stopwords
stopwords=stopwords.words('english')

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
#chatbot
import random 
#translate
!pip install translate
from translate import Translator
#timer
import threading
#save checkpoints
import torch

print(tf.__version__)

if tf.test.gpu_device_name(): 
  print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))
    
else:
  print("Please install GPU version of TF")

#remove emoji
def remove_emoji(text):
     emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
     return emoji_pattern.sub(r'', text)

def remove_url(text):
  url_pattern  = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
  return url_pattern.sub(r'', text)
# converting return value from list to string

def clean_text(text ):
  delete_dict = {sp_character: '' for sp_character in string.punctuation} 
  delete_dict[' '] = ' ' 
  table = str.maketrans(delete_dict)
  text1 = text.translate(table)
  #print('cleaned:'+text1)
  textArr= text1.split()
  text2 = ' '.join([w for w in textArr if ( not w.isdigit() and  ( not w.isdigit() and len(w)>2))]) 
  return text2.lower()

# ouvrir la base des données qui est déja importer
df= pd.read_csv("/content/2020-12-31-DynamicallyGeneratedHateDataset-entries-v0.1.csv",error_bad_lines=False)
 
df.head() #visualisation de la base des donnees

#supprimer les colonnes inutiles: 
df.pop('model_wrong')
df.pop('db.model_preds')
df.pop('round')
df.pop('split')
df.pop('annotator')
df.pop('status')
df.pop('type')

df.head()

def tokenization_stopwords_stemm_Lemmatisation (text):
  tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
  tokens = [token for token in tokens if token not in stopwords]
  stemmer = PorterStemmer()
  tokens = [stemmer.stem(word) for word in tokens]
  tagged_corpus = pos_tag(tokens)
  Noun_tags = ['NN','NNP','NNPS','NNS']
  Verb_tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
  lemmatizer = WordNetLemmatizer()
  def prat_lemmatize(token,tag):
    if tag in Noun_tags:
      return lemmatizer.lemmatize(token,'n')
    elif tag in Verb_tags:
      return lemmatizer.lemmatize(token,'v')
    else:
      return lemmatizer.lemmatize(token,'n')
  pre_proc_text =   " ".join([prat_lemmatize(token,tag) for token,tag in tagged_corpus])

  return pre_proc_text

#preprocess the data
#split data set 80% to train and 20% to test
train_data,test_data=model_selection.train_test_split(df,test_size=0.2)

train_data.dropna(axis = 0, how ='any',inplace=True) 
train_data['Num_words_text'] = train_data['text'].apply(lambda x:len(str(x).split())) 
mask = train_data['Num_words_text'] >2
train_data = train_data[mask]
print('-------Train data--------')
print(train_data['label'].value_counts())
print(len(train_data))
print('-------------------------')
max_train_sentence_length  = train_data['Num_words_text'].max()

train_data['text'] = train_data['text'].apply(remove_emoji)
train_data['text'] = train_data['text'].apply(remove_url)
train_data['text'] = train_data['text'].apply(clean_text)
train_data['text'] = train_data['text'].apply(tokenization_stopwords_stemm_Lemmatisation)
#vectorizer.fit(train_data['text'] )
#train_data['text']  =vectorizer.fit_transform(train_data['text'] )

test_data.dropna(axis = 0, how ='any',inplace=True) 
test_data['Num_words_text'] = test_data['text'].apply(lambda x:len(str(x).split())) 

max_test_sentence_length  = test_data['Num_words_text'].max()

mask = test_data['Num_words_text'] >2
test_data = test_data[mask]

print('-------Test data--------')
print(test_data['label'].value_counts())
print(len(test_data))
print('-------------------------')

test_data['text'] = test_data['text'].apply(remove_emoji)
test_data['text'] = test_data['text'].apply(remove_url)
test_data['text'] = test_data['text'].apply(clean_text)
test_data['text'] = test_data['text'].apply(tokenization_stopwords_stemm_Lemmatisation)
#vectorizer.fit(test_data['text'] )
#test_data['text']  =vectorizer.fit_transform(test_data['text'] )



print('Train Max Sentence Length :'+str(max_train_sentence_length))
print('Test Max Sentence Length :'+str(max_test_sentence_length))
#all_sentences = train_data['text'].tolist() + test_data['text'].tolist()

print(train_data['text'])

print(test_data['text'])

#split the training data into train and validation datasets
num_words = 20000
tokenizer = Tokenizer(num_words=num_words,oov_token="unk")
tokenizer.fit_on_texts(train_data['text'].tolist())
#print(str(tokenizer.texts_to_sequences(['xyz how are you'])))

print(x)

X_train, X_valid, y_train, y_valid = train_test_split(train_data['text'].tolist(),\
                                                       train_data['label'].tolist(),\
                                                        test_size=0.1,\
                                                        stratify = train_data['label'].tolist(),\
                                                        random_state=0)
print('Train data len:'+str(len(X_train)))
print('Class distribution'+str(Counter(y_train)))
print('Valid data len:'+str(len(X_valid)))
print('Class distribution'+ str(Counter(y_valid)))

x_train = np.array( tokenizer.texts_to_sequences(X_train) )
x_valid = np.array( tokenizer.texts_to_sequences(X_valid) )
x_test  = np.array( tokenizer.texts_to_sequences(test_data['text'].tolist()) )
  
x_train = pad_sequences(x_train, padding='post', maxlen=20)
x_valid = pad_sequences(x_valid, padding='post', maxlen=20)
x_test = pad_sequences(x_test, padding='post', maxlen=20)
    
print(x_train[0])
   
le = LabelEncoder()
    
train_labels = le.fit_transform(y_train)
train_labels = np.asarray( tf.keras.utils.to_categorical(train_labels))
#print(train_labels)
valid_labels = le.transform(y_valid)
valid_labels = np.asarray( tf.keras.utils.to_categorical(valid_labels))
    
test_labels = le.transform(test_data['label'].tolist())
test_labels = np.asarray(tf.keras.utils.to_categorical(test_labels))
list(le.classes_)

train_ds = tf.data.Dataset.from_tensor_slices((x_train,train_labels))
valid_ds = tf.data.Dataset.from_tensor_slices((x_valid,valid_labels))
test_ds = tf.data.Dataset.from_tensor_slices((x_test,test_labels))

print(X_train)

print(X_train)
vectorizer.fit(X_train )
X_train =vectorizer.fit_transform(X_train )
print('---------------------x_train_____________________',X_train)

print ('--------------------y_train-----------',y_train)
"""vectorizer.fit(y_train )
y_train =vectorizer.fit_transform(y_train )
print ('--------------------y_train-----------',y_train)"""

print ('--------------------train_labels-----------',train_labels)

print ('--------------------test_labels-----------',test_labels)

print('----------------------------------X_train---------------------',X_train)

print('----------------------------------X_test---------------------',x_test)
"""vectorizer.fit(x_test )
x_test =vectorizer.fit_transform(x_test )
print('----------------------------------X_test---------------------',x_test)
"""

print(y_train[:10])
train_labels = le.fit_transform(y_train)
print('Text to number')
print(train_labels[:10])
train_labels = np.asarray( tf.keras.utils.to_categorical(train_labels))
print('Number to category')
print(train_labels[:10])

count =0
print('===========Train dataset ======')
for value,label in train_ds:
  count +=1
  print(value,label)
  if count ==2:
    break
count =0
print('===========Validation dataset ======')
for value,label in valid_ds:
  count +=1
  print(value,label)
  if count ==2:
    break

print('===========Test dataset ======')
for value,label in train_ds:
  count +=1
  print(value,label)
  if count ==2:
    break

print('train_labels')
print(train_labels[:10])
print('x_train')
print(x_train[:10])
print('test_labels')
print(test_labels[:10])
print('x_test')
print(x_test[:10])

#model
max_features=20000
embedding_dim=64
sequence_length=40

"""model.add(tf.keras.layers.LSTM(32, return_sequences=True, stateful=False, input_shape = (20,85,1)))
model.add(tf.keras.layers.LSTM(20))
model.add(tf.keras.layers.Dense(nb_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
model.summary()
print("Train...")
model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=50, validation_data=(X_test, y_test))"""

model =tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(max_features +1, embedding_dim,input_length=sequence_length ,\
                                    embeddings_regularizer = regularizers.l2(0.0005)))

model.add(tf.keras.layers.Conv1D(128,1,activation='relu' ,\
                                 kernel_regularizer = regularizers.l2(0.0005) ,\
                                 bias_regularizer = regularizers.l2(0.0005)))
model.add(tf.keras.layers.GlobalMaxPooling1D())


model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(2,activation='sigmoid',\
                                kernel_regularizer=regularizers.l2(0.001),\
                                bias_regularizer=regularizers.l2(0.001),))

model.summary()
model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),optimizer='Nadam',metrics=["CategoricalAccuracy"])

#save a checkpoint
torch.save(model.state_dict(), 'checkpoint.pth')

# download checkpoint file
files.download('checkpoint.pth')"""

epochs =25
model.fit(x_train, train_labels,
          batch_size=128,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test,test_labels))

#evaluation du model
score = model.evaluate(x_test, test_labels, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#courbe de model
plt.plot(history.history['categorical_accuracy'], label=' (training data_categorical_accuracy)')
plt.plot(history.history['val_categorical_accuracy'], label='CategoricalCrossentropy (validation data_val_categorical_accuracy)')
plt.title('categorical_accuracy for Text Classification')
plt.ylabel('categorical_accuracy value')
plt.legend(loc="upper left")
plt.show()
"""
plt.plot(history.history['loss'], label=' training data')
plt.plot(history.history['val_loss'], label='validation data)')
plt.title('Loss for Text Classification')
plt.ylabel('Loss value')
plt.xlabel('No. epoch')
plt.legend(loc="upper left")
plt.show()
"""

print(test_data['pred_label'])

#generate perdiction (probabilities of the output of the last layer)
#on test_data using predict
print("generate predictions for all samples")
predictions=model.predict(x_test)
print('prediction',predictions)
predict_results = predictions.argmax(axis=1)
print('predict_results',predict_results)

test_data['pred_label']= predict_results
test_data['pred_label'] = np.where((test_data.pred_label == '0'),'not_hate',test_data.pred_label)
test_data['pred_label'] = np.where((test_data.pred_label == '1'),'hate',test_data.pred_label)

labels=['not_hate','hate']
print(classification_report(test_data['label'].tolist(),test_data['pred_label'].tolist(),labels=labels))

#test sur un exemple
exemp="good ...---*** is"
print('------------------exemp-------------',exemp)
exemp=remove_emoji(exemp)
print('------------------exemp_no_emoji-------------',exemp)
exemp=remove_url(exemp)
print('------------------exemp_no_url-------------',exemp)
exemp=clean_text(exemp)
print('------------------exemp_cleaned-------------',exemp)
exemp=tokenization_stopwords_stemm_Lemmatisation(exemp)
print('------------------exemp_token_lem_sem-------------',exemp)
tokenizer = Tokenizer(num_words=num_words,oov_token="unk")
tokenizer.fit_on_texts(exemp)
x= tokenizer.texts_to_sequences(exemp)
print('------------------exemp_vect-------------',x)

final_x=[]
for i in x :
  for j in i:
    final_x.append(j)
print('------------------final_x-------------',final_x)

#my_array=le.transform(x.tolist())

predictions=model.predict(final_x)
print('--------------------------predictions-------------',predictions)
pred_class=np.argmax(model.predict(final_x), axis=-1)
print('--------------------------pred_class-------------',pred_class)
count_hate=0
count_not_hate=0
for i in pred_class:
  if i == 1:
    count_hate +=1
  else:
    count_not_hate +=1
print ('count_hate',count_hate)
if count_hate>count_not_hate:
  print('it s a hate ')
else:
  print('it s not hate ')

######################## CHATBOT###############################""

!pip install fbchat

#description chatbot
#import libraries
!pip install -U scikit-learn
!pip install nltk
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt',quiet=True)

def response(user_response):
  
  user_response=remove_emoji(user_response)
  print('------------------user_response_no_emoji-------------',user_response)
  user_response=remove_url(user_response)
  print('------------------user_response_no_url-------------',user_response)
  user_response=clean_text(user_response)
  print('------------------user_response_cleaned-------------',user_response)
  user_response=tokenization_stopwords_stemm_Lemmatisation(user_response)
  print('------------------user_response_token_lem_sem-------------',user_response)
  tokenizer = Tokenizer(num_words=num_words,oov_token="unk")
  tokenizer.fit_on_texts(user_response)
  user_response= tokenizer.texts_to_sequences(user_response)
  print('------------------user_response_vect-------------',user_response)

  final_user_response=[]
  for i in user_response :
    for j in i:
      final_user_response.append(j)
  print('------------------final_user_response-------------',final_user_response)

  predictions=model.predict(final_user_response)
  print('--------------------------predictions-------------',predictions)
  pred_class=np.argmax(model.predict(final_user_response), axis=-1)
  print('--------------------------pred_class-------------',pred_class)
  count_hate=0
  count_not_hate=0
  for i in pred_class:
    if i == 1:
      count_hate +=1
    else:
      count_not_hate +=1
  print ('count_hate',count_hate)
  print ('count_not_hate',count_not_hate)

  if count_hate>count_not_hate:
   return print('it s a hate ')
   
  else:
    return print('it s not hate ')

#exemple de test
user_response ='kill muslim'
print(response(user_response))

def greeting(user_response):
  GREETING_INPUTS = ("hello", "hi", "greetings","Is anyone there? ","sup", "what's up","hey")
  GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there","hi! how can I help you?", "hello", "I am glad! You are talking to me"]
  NAME_INPUTS=("what is your name", "what should I call you", "whats your name?")
  NAME_RESPONSES= ["You can call me DASH.", "I'm DASH!"]
  Q_INPUTs=("what can you do?","what do you offer?","what's your service")
  Q_RESPONSES=["I'm DASH ,an intelligent chatbot made to help you analyse your data if it's a hate threat or not"]

 
  for word in user_response.split():
    if word.lower() in GREETING_INPUTS:
      return random.choice(GREETING_RESPONSES)
    if word.lower() in NAME_INPUTS:
      return random.choice(NAME_RESPONSES)
    if word.lower() in Q_INPUTs:
      return random.choice(Q_RESPONSES)

def translate(text,language):
  trans_french=Translator(from_lang="en",to_lang="fr")
  trans_arabic=Translator(from_lang="en",to_lang="arabic")
  trans_italian=Translator(from_lang="en",to_lang="it")
  trans_japanese=Translator(from_lang="en",to_lang="ja")
  trans_deutsh=Translator(from_lang="en",to_lang="de")

  #print('entrez votre donnée à traduire')
  #x=input()
  #print('choisir votre langue de traduction')
  #language_choice=input()
  if language.lower() in { "fr","français","french"}:
    return trans_french.translate(text)
  elif language.lower() in { "ar","arabe","arabic"}:
    return trans_arabic.translate(text)
  elif language.lower() in { "it","italian","italien"}:
    return trans_italian.translate(text)
  elif language.lower() in { "ja","japonais","japanese"}:
    return trans_japanese.translate(text)
  elif language.lower() in { "de","allemand","deutsh"}:
    return trans_deutsh.translate(text)
  #print('votre résultat est :',result)

#relate code chatbot to fb account
from fbchat import Client,log
from fbchat.models import *
class jarvis(Client):
  def onMessage(sel,author_id=None,message_object=None,thread=None,thread_id=None,thread_type=ThreadType.USER,**kwargs):
    #mark msg as read
    self.markAsRead(author_id)
    #print info on console
    log.info("Message {} from {} in{}".format(message_object,thread_id,thread_type))
    msgText=message_object.text

    reply='hello world'
    #send msg
    if author_id !=self.uid:
      self.send(Message(text=reply),thread_id=thread_id,thread_type=thread_type)

    self.markAsDelivered(author_id,thread_id)
username="siwarjemai0@gmail.com"
password="dashdash"
client =jarvis(username,password)
#liten for new msg
client.listen()

#load the checkpoint
#model.load_state_dict(state_dict)
flag=True
print("DASH: My name is DASH. I will answer your queries. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if (user_response!='bye'):
        if (user_response=='thanks' or user_response=='thank you' or user_response=='thx' ):
            #flag=False
            print("DASH: You are welcome..")
            timer = threading.Timer(2.0, "do you need another help?")
            print('you can tap YES to continue or NO to stop!')

            timer.start()
            x1=input()
            x1=x1.lower()
            if x1 =='yes':
              #flag=False
              print('enter your data to treat it ')
            else :
              #flag=False
              print('DASH: See you later ! But Don t forget to wear you mask !..')

        elif (greeting(user_response)!=None):
          #flag=False
          print("DASH: "+greeting(user_response))
        else:
          #flag=False
 #         print("DASH: ",end="")
          print(response(user_response))
          if( response(user_response)=='it s not hate'):
            print('do you want translate your text?')
            print('you can tap YES to continue or NO to stop!')
            x2=input()
            x2=x2.lower()
            if x2=='yes':
              #flag=False
              print('to which langauage do you want to translate you text?')
              y=input()
              print(translate(user_response,y.lower()))
            else:
              #flag=False
              print('DASH: See you later ! But Don t forget to wear you mask !..')
          else:
            print('WARNING! it s an abuse, STOP these assaults ,don t hesitate to file a complaint')
            timer = threading.Timer(2.0, "do you need another help?")
            print('you can tap YES to continue or NO to stop!')
            x1=input()
            if x1 =='yes':
              #flag=False
              print('enter your data to treat it ')
              user_response=input()
            else :
              #flag=False
              print('DASH: See you later ! But Don t forget to wear you mask !..')

          #sent_tokens.remove(user_response)
    else:
        flag=False
        print("DASH: Bye! But Don't forget to wear you mask !..")