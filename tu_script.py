from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7726763215:AAGRAODvMB13AMHWhn3DCGWp1A7ca9nTXZk"  async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envía /codigo para recibir tu código.")

async def enviar_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    codigo = "Código123"  # Este es un ejemplo de código
    await update.message.reply_text(f"Tu código es: {codigo}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("codigo", enviar_codigo))

    # Comienza a recibir actualizaciones
    app.run_polling()

if __name__ == '__main__':
    main()