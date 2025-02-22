from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import logging

TOKEN = "7598489828:AAEEhPX4cR4GMndMJS0tqVA1lKRh3FM8AtM"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("interes"))
async def calcular_interes_compuesto(message: types.Message):
    try:
        _, capital, tasa, periodos = message.text.split()
        capital = float(capital)
        tasa = float(tasa) / 100  # Convertimos porcentaje a decimal
        periodos = int(periodos)

        monto_final = capital * ((1 + tasa) ** periodos)
        total_invertido = sum(capital * ((1 + tasa) ** i) for i in range(periodos))

        mensaje = (
            f"📈 *Cálculo de Interés Compuesto*\n"
            f"💵 *Capital inicial:* ${capital:,.2f}\n"
            f"📊 *Tasa de interés:* {tasa * 100:.2f}%\n"
            f"⏳ *Número de períodos:* {periodos}\n"
            f"💰 *Monto final:* ${monto_final:,.2f}\n"
            f"📥 *Total invertido con aportes:* ${total_invertido:,.2f}"
        )
    except ValueError:
        mensaje = "⚠️ Uso incorrecto. Formato: /interes [capital] [tasa] [periodos]\nEjemplo: /interes 50 8 12"

    await message.answer(mensaje, parse_mode="Markdown")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
