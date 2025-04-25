from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "7726763215:AAGRAODvMB13AMHWhn3DCGWp1A7ca9nTXZk"  

def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! Envía /codigo para recibir tu código.")

def enviar_codigo(update: Update, context: CallbackContext):
    # Este es un ejemplo de código
    codigo = "Código123"  
    update.message.reply_text(f"Tu código es: {codigo}")

def main():
    updater = Updater(TOKEN)

    # Añadir manejadores de comandos
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("codigo", enviar_codigo))

    # Comienza a recibir actualizaciones
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()