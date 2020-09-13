from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

greetings = [
    "Mambo?",
    "Poa",
    "Niaje?",
    "Safi tu",
    "Habari yako?",
    "Nzuri tu! sijui wewe",
    "Unajiskiaje?",
    "Najiskia vizuri",
    "Habari ya jioni?",
    "Nzuri! wewe je?",
]
bot = ChatBot(
    "Hina",
    )

trainer = ListTrainer(bot)

trainer.train(greetings)

print("I am Hina chatterbot ready to chat with you")
response = bot.get_response(input())
print(response)