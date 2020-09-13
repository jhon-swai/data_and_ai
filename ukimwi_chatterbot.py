from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json
import string

stopwords = ["akasema","alikuwa","alisema","baada","basi","bila","cha","chini","hadi","hapo","hata","hivyo","hiyo","huku","huo","ili","ilikuwa","juu","kama","karibu","katika","kila","kima","kisha","kubwa","kutoka","kuwa","kwa","kwamba","kwenda","kwenye","la","lakini","mara","mdogo","mimi","mkubwa","mmoja","moja","muda","mwenye","na","naye","ndani","ng","ni","nini","nonkungu","pamoja","pia","sana","sasa","sauti","tafadhali","tena","tu","vile","wa","wakati","wake","walikuwa","wao","watu","wengine","wote","ya","yake","yangu","yao","yeye","yule","za","zaidi","zake"]


# Function for preprocessing the input data
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

# Function for cleaning the ouput
def clean_output(text):
    text = text.replace("\n" , " ")
    text = text.capitalize()
    return text

# creating a question list 
questions_list = []
def conv_list_of_qns(lst):
    global questions_list
    for i in range(len(lst)):
        questions_list.append( lst[i]["1"] )

#crearing answer list 
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

cleaned_questions_list  = list( map(clean_output, questions_list)  ) 
cleaned_answers_list = list( map(clean_output, answers_list))

ukimwi_conversation = []

# mixing list values 
for i in range(len(questions_list)):
    ukimwi_conversation.append(cleaned_questions_list[i])
    ukimwi_conversation.append( cleaned_answers_list[i] )

greetings = [
    "Mambo?",
    "Poa",
    "Niaje?",
    "Safi tu",
    "oi?",
    "niambie",
    "ishu vipi?",
    "safi tu",
    "Habari yako?",
    "Nzuri tu! sijui wewe",
    "Unajiskiaje?",
    "Najiskia vizuri",
    "Habari ya jioni?",
    "Nzuri! wewe je?",
]

bot = ChatBot(
    "Hina",
    logic_adapters = [
        'chatterbot.logic.BestMatch'
    ]
    #database_uri = './ukimwi.sqlite3'
    )

trainer = ListTrainer(bot)

for item in (greetings, ukimwi_conversation):
    trainer.train(item)

print("This is Hinaa bot ready to answer your questions")
while True:
    try: 
        print("Ask your question")
        response = bot.get_response(input() )
        print(response)
    
    except(KeyboardInterrupt, EOFError, SystemExit):
        break

