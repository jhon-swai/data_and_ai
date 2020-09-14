from flask import Flask, request, jsonify

# This bot is based on json file processing 
import random
import string
import nltk
import numpy as np
import Levenshtein
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from difflib import SequenceMatcher


app = Flask(__name__)
# list of swahili stopwords 
stopwords = ["akasema","alikuwa","alisema","baada","basi","bila","cha","chini","hadi","hapo","hata","hivyo","hiyo","huku","huo","ili","ilikuwa","juu","kama","karibu","katika","kila","kima","kisha","kubwa","kutoka","kuwa","kwa","kwamba","kwenda","kwenye","la","lakini","mara","mdogo","mimi","mkubwa","mmoja","moja","muda","mwenye","na","naye","ndani","ng","ni","nini","nonkungu","pamoja","pia","sana","sasa","sauti","tafadhali","tena","tu","vile","wa","wakati","wake","walikuwa","wao","watu","wengine","wote","ya","yake","yangu","yao","yeye","yule","za","zaidi","zake"]

nltk.download('punkt', quiet=True)


# a Function to perform clean all the newline symbols
def clean_string(text):
    #Removing the newline replacing it with space
    text = text.replace("\n", " ")

    # removing punctuations
    text = ''.join([word for word in text if word not in string.punctuation])

    # Converting to lower case
    text = text.lower() 

    #remove stopwords 
    text = ' '.join([word for word in text.split() if word not in stopwords])
    
    return text

def remove_stopwords(text):
    # have to be in small letters
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text


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
    sFileReadList = json.loads(sFileRead)

    #converting the files to a list of questions and answers 
    conv_list_of_qns(sFileReadList)
    conv_list_of_ans(sFileReadList)

json_file_manager()

cleaned_questions_list  = list( map(clean_string, questions_list)  ) 
# cleaned_questions_list = questions_list
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
def clean_output(text):
    text = text.replace("\n" , " ")
    text = text.capitalize()
    return text

# using levenshtein distance for single words 
# not used yet
def levenshtein_distance_f(text):
    index = 10
    for i in range(len(questions_list)):
        # need modification to only compare single word values from the questions list 
        lScore = Levenshtein.distance( cleaned_questions_list[i],text )
        if lScore <=3 :
            index = i
            break
    return index

def sequence_matcher_f(user_input_str):
    for i in cleaned_questions_list:
        sim_score =  SequenceMatcher(None, user_input_str, i).ratio()
        if ( sim_score ) > 0.5 :
            ind = cleaned_questions_list.index(i)
            return answers_list[ind]
    return None


# create bot response
def bot_response(user_input):  
    #cleaning user data 
    cleaned_user_input = clean_string(user_input)
    
    cleaned_questions_list.append(cleaned_user_input)

    # appending this to avoid index out of bound error and will be removed at the end
    answers_list.append( user_input.lower() )
    
    
    cm  = CountVectorizer().fit_transform(cleaned_questions_list)
    
    # get the similarity score
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarty_scores_list = similarity_scores.flatten()
    
    # to get index of the highest element
    index = index_sort(similarty_scores_list)
    
    # removing the index which is obviously the user's own input
    index.remove(max(index))
    response_flag = 0
    
    #for counting the number of scores that are above 0
    j = 0
    
    #initilize the bot response to an empty string
    bot_response = ''
    for i in range(len(index)):
        if similarty_scores_list[index[i]] > 0.4:
            bot_response = bot_response + " " + clean_output( answers_list[index[i]] )
            response_flag = 1 
            
            j = j+1
        # limit the number of output values         
        if j > 0:
            break
    if response_flag == 0:
        bot_response = bot_response + ' ' + "I apologize, I don\'t understand"
    
    # removing the added user input
    # cleaned_questions_list.remove(clean_string(user_input) )
    cleaned_questions_list.remove( cleaned_user_input )
    answers_list.remove(user_input.lower())
    return bot_response

exit_list = ['exit', 'bye', 'end']

def word_count(input_text):
    input_text = input_text.split()
    return len(input_text)

def user_input_f(text):
    print("This is Doc Bot ready to answer your questions: \n \t Enter bye,end or exit to leave")
    
    while(True):
        user_input = text.lower()
        
        if user_input in exit_list:
            print('Doc Bot: ' +  "Bye")
            break
        else:
            if greeting_response(user_input) != None:
                return ('Doc Bot: ' + greeting_response(user_input))
            else:
                if word_count(user_input) <= 1:
                    bot_answer  = sequence_matcher_f(user_input)
                else:
                    bot_answer = bot_response(user_input)

                return ('Doc Bot: ' + bot_answer )

@app.route("/", methods= ["POST", "GET"])
def welcome():
    if request.method == "POST":
        return "That was a post request"
    if request.method == "GET":
        return "Welcome to my Flask page" + "Get request"

@app.route("/name")
def myName():
    return "My name is Chinaa"


qa = {
    "ukimwi ni nini": "Upungufu wa kinga mwilini.",
    "vvu ni nini": "Virusi vya ukimwi ni virusi vinavyosambwazwa ugonjwa"
}

@app.route("/ask", methods=["POST"])
def ask():
    question = request.get_json()["question"]
    answer_value = user_input_f(question)
    return answer_value
