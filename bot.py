from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Função que será chamada quando o comando /start for enviado
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá, eu sou seu bot!")

def main():
    # Substitua 'YOUR_API_KEY' pela chave da sua API do bot Telegram
    updater = Updater("8016591601:AAGc6f276J2aWWS0ti_JV5uo7K8ouwvWhno", use_context=True)

    # Obtendo o dispatcher para adicionar manipuladores
    dispatcher = updater.dispatcher

    # Adicionando o manipulador de comando para /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Iniciando o bot
    updater.start_polling()

    # Mantendo o bot rodando
    updater.idle()

if __name__ == "__main__":
    main()
