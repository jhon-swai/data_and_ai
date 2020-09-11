# This bot is based on json file processing 

from newspaper import Article
import random
import string
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import json

warnings.filterwarnings('ignore')

# list of swahili stopwords 
stopwords = ["akasema","alikuwa","alisema","baada","basi","bila","cha","chini","hadi","hapo","hata","hivyo","hiyo","huku","huo","ili","ilikuwa","juu","kama","karibu","katika","kila","kima","kisha","kubwa","kutoka","kuwa","kwa","kwamba","kwenda","kwenye","la","lakini","mara","mdogo","mimi","mkubwa","mmoja","moja","muda","mwenye","na","naye","ndani","ng","ni","nini","nonkungu","pamoja","pia","sana","sasa","sauti","tafadhali","tena","tu","vile","wa","wakati","wake","walikuwa","wao","watu","wengine","wote","ya","yake","yangu","yao","yeye","yule","za","zaidi","zake"]

nltk.download('punkt', quiet=True)

# get the article
article = Article("https://sw.wikipedia.org/wiki/Ukimwi")
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentence_list = nltk.sent_tokenize(text) # a list of sentences

# a Function to perform clean all the newline symbols
def clean_string(text):
    #Removing the newline replacing it with space
    text = text.replace("\n", " ")
    # Converting to lower case
    text = text.lower()    
    return text

def remove_stopwords(text):
    # have to be in small letters
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

#built in map function instead of loop to perform the sentence transformation
cleaned_sentence_list = list( map(clean_string, sentence_list))

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

questions_list = []
def conv_list_of_qns(lst):
    global questions_list
    for i in range(len(lst)):
        questions_list.append( lst[i]["1"] )

answers_list = []
def conv_list_of_ans(lst):
    global answers_list
    for i in range(len(lst)):
        answers_list.append( lst[i]["2"] )

def json_file_manager():
    sourceFile = open("swahili_qna.json", 'rt')
    #We now have a list of all the questions and answers ie list of dictionaries
    sFileRead = sourceFile.read()

    #converting the files to a list of questions and answers 
    conv_list_of_qns(sFileRead)
    conv_list_of_ans(sFileRead)


# a function to return a random greeting response to a users greetings 
def greeting_response(text):
    text = text.lower()
    
    #Bots random greetings 
    bot_greetings = ['poa', 'baridi', 'safi', 'kama kawa']
    
    #user greetings
    
    user_greetings = ['mambo', 'vipi', 'vip', 'niaje']
    
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)
    return None
        
# create bot response
def bot_response(user_input):  
    #cleaning user data 
    cleaned_user_input = clean_string(user_input)
    
    cleaned_user_input_length = len(cleaned_user_input)
    
    cleaned_sentence_list.append(cleaned_user_input)
    sentence_list.append( user_input.lower() )
    
    
    cm  = CountVectorizer().fit_transform(cleaned_sentence_list)
    
    # get the similarity score
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarty_scores_list = similarity_scores.flatten()
    
    # to get index of the highest element
    index = index_sort(similarty_scores_list)
    
    # removing the first index which is obviously the user's own input
    index = index[1:]
    response_flag = 0
    
    #for counting the number of scores that are above 0
    j = 0
    
    #initilize the bot response to an empty string
    bot_response = ''
    for i in range(len(index)):
        if similarty_scores_list[index[i]] > 0.0:
            bot_response = bot_response + " " + sentence_list[index[i]]
            response_flag = 1 
            
            j = j+1
            
#         checking for single words 
#         could be compared to user_input_length instead
#         if cleaned_user_input_length <= 1:
#             bot_response = bot_response + " not enough data to get distinct results"
#             break
            
        if j > 2:
            break
    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I don\'t understand"
    
    # removing the added user input
    cleaned_sentence_list.remove(clean_string(user_input) )
    sentence_list.remove(user_input.lower())
    
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
                bot_answer = bot_response(user_input)
                
                print('Doc Bot: ' + bot_answer )