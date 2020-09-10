from newspaper import Article
import random
import string
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

stopwords = stopwords.words('english')

nltk.download('punkt', quiet=True)

# get the article
article = Article("https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521")
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentence_list = nltk.sent_tokenize(text) # a list of sentences

# a Function to perform data cleaning 

def clean_string(text):
    # Removing punctuation from a given string
    text = ''.join([word for word in text if word not in string.punctuation])
    
    # Converting to lower case
    text = text.lower()
    
    # removing stopwords
    text = ' '.join([word for word in text.split() if word not in stopwords])
    
    return text

#built in map function instead of loop to perform the sentence transformation
cleaned_sentence_list = list( map(clean_string, sentence_list))

# a function to return a random greeting response to a users greetings 
def greeting_response(text):
    text = text.lower()
    
    #Bots random greetings 
    bot_greetings = ['howdy', 'hi', 'hey', 'hello', 'hola']
    
    #user greetings
    
    user_greetings = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']
    
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None
        
def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0,length))
    
    x = list_var
    for i in range (length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
                
    return list_index
# create bot response
def bot_response(user_input):
    
    #cleaning user data 
    cleaned_user_input = clean_string(user_input)
    cleaned_sentence_list.append(cleaned_user_input)
    
    bot_response = ''
    cm  = CountVectorizer().fit_transform(cleaned_sentence_list)
    
    # get the similarity score
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarty_scores_list = similarity_scores.flatten()
    
    # to get index of the highest element first list
    index = index_sort(similarty_scores_list)
    
    # removing the first index which is obviously the user's own input
    index = index[1:]
    response_flag = 0
    
    #for counting the number of scores that are above 0
    j = 0
    
    for i in range(len(index)):
        if similarty_scores_list[index[i]] > 0.0:
            bot_response = bot_response + " " + sentence_list[index[i]]
            response_flag = 1 
            
            j = j+1
            
        if j > 2:
            break
    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I don\'t understand"
    
    # removing the added user input
    cleaned_sentence_list.remove(cleaned_user_input)
    
    return bot_response

exit_list = ['exit', 'bye', 'end']

def user_input_f():
    print("This is Doc Bot ready to answer your questions ")
    
    while(True):
        user_input = input()
        
        if user_input.lower() in exit_list:
            print('Doc Bot: ' +  "Bye")
            break
        else:
            if greeting_response(user_input) != None:
                print('Doc Bot: ' + greeting_response(user_input))
            else:
                print('Doc Bot: ' +  bot_response(user_input) )

user_input_f()