import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import random

# Carregar as variáveis do .env
load_dotenv()

# Criar o app do Flask
app = Flask(__name__)

# Criação do bot com a chave da API
bot = Bot(token=os.getenv("TELEGRAM_API_KEY"))

# Criar Dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)

# Dicionário para armazenar os jogadores
jogadores = {}

# Função para iniciar o bot
def start(update: Update, context):
    update.message.reply_text("🏀 Bem-vindo ao NBASimulatorBot!\nDigite /criar_jogador para começar sua jornada.")

# Função para criar um jogador
def criar_jogador(update: Update, context):
    chat_id = update.message.chat_id
    update.message.reply_text("Digite o nome do seu jogador:")
    context.user_data['esperando_nome'] = True

# Função para escolher foco inicial
def escolher_foco(update: Update, context):
    chat_id = update.message.chat_id
    jogadores[chat_id] = {'nome': update.message.text, 'temporadas': 0, 'overall': 60, 'foco': ''}
    update.message.reply_text("Escolha seu foco inicial: \n1 - Arremessos de 3 pontos\n2 - Enterradas\n3 - Defesa\n4 - Playmaking")
    context.user_data['esperando_foco'] = True

# Função para iniciar uma temporada
def iniciar_temporada(update: Update, context):
    chat_id = update.message.chat_id
    if chat_id not in jogadores:
        update.message.reply_text("Você ainda não criou um jogador. Use /criar_jogador primeiro.")
        return
    
    jogador = jogadores[chat_id]
    jogador['temporadas'] += 1
    
    # Simulação de estatísticas
    pontos = random.randint(10, 30)
    assistencias = random.randint(2, 10)
    rebotes = random.randint(3, 12)
    lesao = random.random() < 0.2  # 20% de chance de lesão
    
    resultado = f"🏀 Temporada {jogador['temporadas']} concluída!\n" \
               f"Nome: {jogador['nome']}\n" \
               f"Pontos por jogo: {pontos}\n" \
               f"Assistências por jogo: {assistencias}\n" \
               f"Rebotes por jogo: {rebotes}\n"
    
    if lesao:
        resultado += "🚑 Você sofreu uma lesão e perdeu parte da temporada!"
    
    update.message.reply_text(resultado)

# Função para capturar mensagens e processar o fluxo
def mensagem(update: Update, context):
    chat_id = update.message.chat_id
    if context.user_data.get('esperando_nome', False):
        escolher_foco(update, context)
        context.user_data['esperando_nome'] = False
        return
    
    if context.user_data.get('esperando_foco', False):
        foco = update.message.text
        if foco in ['1', '2', '3', '4']:
            jogadores[chat_id]['foco'] = foco
            update.message.reply_text("🏀 Jogador criado com sucesso! Use /temporada para iniciar sua primeira temporada.")
        else:
            update.message.reply_text("Escolha uma opção válida (1-4)")
        context.user_data['esperando_foco'] = False
        return

# Rota do Webhook
@app.route(f"/{os.getenv('8016591601:AAGc6f276J2aWWS0ti_JV5uo7K8ouwvWhno')}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Configuração do bot com o Flask
def main():
    from os import environ
    PORT = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

# Configuração de comandos e mensagens
def setup():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("criar_jogador", criar_jogador))
    dispatcher.add_handler(CommandHandler("temporada", iniciar_temporada))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, mensagem))

if __name__ == "__main__":
    setup()
    main()
