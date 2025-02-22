import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp

TOKEN = "7598489828:AAEEhPX4cR4GMndMJS0tqVA1lKRh3FM8AtM"
CHAT_ID = "589359631"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Función para obtener el precio actual de BTC y su ATH desde CoinGecko
async def obtener_precio_y_ath():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            precio_actual = data["market_data"]["current_price"]["usd"]
            maximo_historico = data["market_data"]["ath"]["usd"]
            return precio_actual, maximo_historico

# Función para calcular cuánto invertir según la estrategia escalonada
def calcular_inversion(precio_actual, maximo_historico):
    porcentaje_caida = ((maximo_historico - precio_actual) / maximo_historico) * 100
    inversion = 0

    if 0 <= porcentaje_caida <= 10:
        inversion = porcentaje_caida * 1
    elif 11 <= porcentaje_caida <= 20:
        inversion = 10 + (porcentaje_caida - 10) * 1.5
    elif 21 <= porcentaje_caida <= 30:
        inversion = 25 + (porcentaje_caida - 20) * 2
    elif 31 <= porcentaje_caida <= 40:
        inversion = 45 + (porcentaje_caida - 30) * 2.5
    elif 41 <= porcentaje_caida <= 50:
        inversion = 70 + (porcentaje_caida - 40) * 3

    return min(inversion, 150)  # Máximo de $150 por día

# Manejar el comando /inversion
@dp.message(Command("inversion"))
async def enviar_informe_diario(message: Message):
    precio_actual, maximo_historico = await obtener_precio_y_ath()
    monto_inversion = calcular_inversion(precio_actual, maximo_historico)
    porcentaje_caida = ((maximo_historico - precio_actual) / maximo_historico) * 100

    mensaje = (
        f"📊 *Informe de Inversión BTC*\n"
        f"💰 *Precio actual:* ${precio_actual:,.2f}\n"
        f"📉 *Por debajo del ATH:* {porcentaje_caida:.2f}%\n"
        f"💵 *Monto a invertir:* ${monto_inversion:,.2f}"
    )

    await message.answer(mensaje, parse_mode="Markdown")

# Iniciar el bot
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())