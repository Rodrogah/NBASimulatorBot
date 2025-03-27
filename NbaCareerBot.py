from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# Dicionário para armazenar os jogadores
jogadores = {}

# Função para iniciar o bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🏀 Bem-vindo ao NBASimulatorBot!\nDigite /criar_jogador para começar sua jornada.")

# Função para criar um jogador
def criar_jogador(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text("Digite o nome do seu jogador:")
    context.user_data['esperando_nome'] = True

# Função para escolher foco inicial
def escolher_foco(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    jogadores[chat_id] = {'nome': update.message.text, 'temporadas': 0, 'overall': 60, 'foco': ''}
    update.message.reply_text("Escolha seu foco inicial: \n1 - Arremessos de 3 pontos\n2 - Enterradas\n3 - Defesa\n4 - Playmaking")
    context.user_data['esperando_foco'] = True

# Função para iniciar uma temporada
def iniciar_temporada(update: Update, context: CallbackContext):
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
def mensagem(update: Update, context: CallbackContext):
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

# Configuração do bot
def main():
    updater = Updater("8016591601:AAGc6f276J2aWWS0ti_JV5uo7K8ouwvWhno", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("criar_jogador", criar_jogador))
    dp.add_handler(CommandHandler("temporada", iniciar_temporada))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, mensagem))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
