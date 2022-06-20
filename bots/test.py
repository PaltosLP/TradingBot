
def file(bot, action):
    f = open('log.txt', 'a')
    txt = str(bot) + str(action) 
    f.write(txt)
    f.close()


from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


print("bot"+"get")
