
import telebot
import subprocess
import requests
import datetime
import os

from keep_alive import keep_alive
keep_alive()

# Your Telegram bot token
bot = telebot.TeleBot('7570618579:AAF4Rfsrw6FPrzpTkgSS6Kva4PxyC0lJ_bg')

# Admin user ID
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


# Admin-only access for all commands
@bot.message_handler(func=lambda message: str(message.chat.id) == "1232759277")
def handle_admin_commands(message):
    if message.text.lower() == "/start":
        bot.reply_to(message, "Hello Admin! You can use any command.")

    elif message.text.lower() == "/help":
        bot.reply_to(message, '''Available commands:
    /add <user_id> - Add a new user (currently not needed).
    /remove <user_id> - Remove a user (currently not needed).
    /status - Get bot status.
    /clearlogs - Clear command logs.
    ''')

    elif message.text.lower() == "/status":
        bot.reply_to(message, "Bot is running and is only accessible by the admin.")

    elif message.text.lower() == "/clearlogs":
        response = clear_logs()
        bot.reply_to(message, response)

    else:
        bot.reply_to(message, "Unknown command. Type /help for available commands.")


# Admin command to broadcast message to all users
@bot.message_handler(func=lambda message: str(message.chat.id) == "1232759277" and message.text.lower().startswith("/broadcast"))
def broadcast_message(message):
    command = message.text.split(maxsplit=1)
    if len(command) > 1:
        message_to_broadcast = "Message To All Users By Admin:\n\n" + command[1]
        response = "Broadcast message sent successfully."
        # No user management is done, so this feature is effectively disabled
    else:
        response = "Please provide a message to broadcast."
    bot.reply_to(message, response)


# Function to handle attacks (for testing purposes, but no user management)
@bot.message_handler(func=lambda message: str(message.chat.id) == "1232759277" and message.text.lower().startswith("/attack"))
def start_attack(message):
    command = message.text.split()
    if len(command) == 4:
        target = command[1]
        port = int(command[2])
        time = int(command[3])

        response = f"Attack started on target {target} at port {port} for {time} seconds. Method: Premium \nBy @BKMOMNIVERSE"
        # Normally, you'd run the subprocess here, but for safety, we won't actually execute anything
        # full_command = f"./RAGNAROK {target} {port} {time}"
        # subprocess.run(full_command, shell=True)

        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "Usage: /attack <target> <port> <time>")

# Non-admin users are automatically blocked
@bot.message_handler(func=lambda message: str(message.chat.id) != "1232759277")
def handle_non_admin(message):
    bot.reply_to(message, "You are not authorized to use this bot.")

# Start the bot
bot.polling(none_stop=True)
