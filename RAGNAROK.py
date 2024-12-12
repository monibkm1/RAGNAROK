import telebot
import subprocess
import requests
import datetime
import os

from keep_alive import keep_alive
keep_alive()

# Your Telegram bot token
bot = telebot.TeleBot('7570618579:AAF4Rfsrw6FPrzpTkgSS6Kva4PxyC0lJ_bg')

# Admin user ID (currently not in use)
admin_id = ["1232759277"]

# File to store command logs
LOG_FILE = "log.txt"

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Open to all users now
@bot.message_handler(commands=['start', 'help', 'status', 'clearlogs', 'attack1', 'broadcast', 'mylogs'])
def handle_commands(message):
    user_id = str(message.chat.id)

    if message.text.lower() == "/start":
        bot.reply_to(message, "Hello! You can use the available commands.")

    elif message.text.lower() == "/help":
        bot.reply_to(message, '''Available commands:
    /status - Get bot status.
    /clearlogs - Clear command logs.
    /attack1 <target> <port> <time> - Start a fake attack.
    /broadcast <message> - Broadcast a message to all users.
    /mylogs - View your command logs.
    ''')

    elif message.text.lower() == "/status":
        bot.reply_to(message, "Bot is running and accessible by everyone.")

    elif message.text.lower() == "/clearlogs":
        response = clear_logs()
        bot.reply_to(message, response)

    elif message.text.lower().startswith("/attack1"):
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])

            response = f"Attack started on target {target} at port {port} for {time} seconds. Method: Premium\nBy @BKMOMNIVERSE"
            # Normally, you'd run the subprocess here, but for safety, we won't actually execute anything
            # full_command = f"./RAGNAROK {target} {port} {time}"
            # subprocess.run(full_command, shell=True)

            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Usage: /attack1 <target> <port> <time>")

    elif message.text.lower().startswith("/broadcast"):
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message to all users:\n\n" + command[1]
            # Broadcast message functionality
            bot.reply_to(message, "Broadcast message sent successfully.")
        else:
            bot.reply_to(message, "Please provide a message to broadcast.")

    elif message.text.lower() == "/mylogs":
        bot.reply_to(message, "Logs for your command usage.")

    else:
        bot.reply_to(message, "Unknown command. Type /help for available commands.")

# Non-admin users are automatically allowed to use the bot (no restriction now)
@bot.message_handler(func=lambda message: True)
def handle_non_admin(message):
    user_id = str(message.chat.id)
    bot.reply_to(message, "You are using the bot.")

# Start the bot
bot.polling(none_stop=True)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''Available commands:
 /attack1 : Method For Bgmi Servers. 
 /rules : Please Check Before Use !!.
 /mylogs : To Check Your Recents Attacks.
 /plan : Checkout Our Botnet Rates.

 To See Admin Commands:
 /admincmd : Shows All Admin Commands.
 By STORM BOT
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome to Your Home, {user_name}! Feel Free to Explore.\nTry To Run This Command : /help\nWelcome To The World's Best Ddos Bot\nBy https://t.me/RAGNAROKCRACKER"
    bot.reply_to(message, response)


@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!
By STORM BOT'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip :
-> Attack Time : 200 (S)
> After Attack Limit : 2 Min
-> Concurrents Attack : 300

Pr-ice List:
per match--> 30 Rs
per hours--> 50 Rs
Day--------> 250 Rs
Week-------> 900 Rs
Month------> 1600 Rs
LifeTimes--> 2000 Rs
By STORM BOT
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

/add <userId> : Add a User.
/remove <userid> Remove a User.
/allusers : Authorised Users Lists.
/logs : All Users Logs.
/broadcast : Broadcast a Message.
/clearlogs : Clear The Logs File.
By https://t.me/BKMOMNIVERSE
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users."
        else:
            response = "Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)




bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)

#By RᴀɢɴᴀʀᴏK Cʀᴀᴄᴋᴇʀs
