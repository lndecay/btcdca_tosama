import asyncio
import schedule
import time
import datetime
import requests
from telegram import Bot

# Configura tu token y chat ID
TOKEN = "7598489828:AAEEhPX4cR4GMndMJS0tqVA1lKRh3FM8AtM"
CHAT_ID = "589359631"

# Inicializa el bot de Telegram
bot = Bot(token=TOKEN)

def obtener_precios():
    """Obtiene el precio actual de BTC, su máximo histórico y los precios de los últimos 7 días desde CoinGecko."""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    try:
        response = requests.get(url)
        data = response.json()
        precio_actual = data["market_data"]["current_price"]["usd"]
        max_historico = data["market_data"]["ath"]["usd"]
        
        # Obtener precios de los últimos 7 días
        url_hist = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
        response_hist = requests.get(url_hist)
        data_hist = response_hist.json()
        precios_7_dias = [p[1] for p in data_hist["prices"]]
        precio_promedio_semanal = sum(precios_7_dias) / len(precios_7_dias)
        
        return precio_actual, max_historico, precio_promedio_semanal
    except Exception as e:
        print(f"Error obteniendo precios: {e}")
        return None, None, None

def calcular_inversion_semanal():
    """Calcula la inversión total de la semana según la estrategia escalonada."""
    precio_actual, max_historico, precio_promedio_semanal = obtener_precios()
    
    if precio_actual is None or max_historico is None:
        return "❌ Error obteniendo precios de Bitcoin."

    porcentaje_caida = ((max_historico - precio_actual) / max_historico) * 100
    total_semanal = 0

    for _ in range(7):  # Se calcula la inversión diaria y se suma por 7 días
        if porcentaje_caida <= 10:
            inversion_diaria = porcentaje_caida * 1
        elif porcentaje_caida <= 20:
            inversion_diaria = (10 * 1) + ((porcentaje_caida - 10) * 1.5)
        elif porcentaje_caida <= 30:
            inversion_diaria = (10 * 1) + (10 * 1.5) + ((porcentaje_caida - 20) * 2)
        elif porcentaje_caida <= 40:
            inversion_diaria = (10 * 1) + (10 * 1.5) + (10 * 2) + ((porcentaje_caida - 30) * 2.5)
        else:  # 41% - 50%
            inversion_diaria = (10 * 1) + (10 * 1.5) + (10 * 2) + (10 * 2.5) + ((porcentaje_caida - 40) * 3)
        
        total_semanal += min(inversion_diaria, 150)  # Aplica el tope diario de $150

    return f"📊 *Inversión Semanal Calculada*\n💰 Monto total recomendado: *${total_semanal:.2f}*\n📉 Caída desde ATH: *{porcentaje_caida:.2f}%*\n📊 Precio promedio semanal: *${precio_promedio_semanal:.2f}*"

async def enviar_mensaje_semanal():
    """Genera y envía el mensaje semanal con la inversión recomendada."""
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    mensaje = (
        f"📅 *Informe Semanal de Inversión* ({fecha_actual})\n\n"
        f"{calcular_inversion_semanal()}\n\n"
        "_Este es un mensaje automático._"
    )
    
    await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")

def ejecutar_asyncio(task):
    """Ejecuta tareas asíncronas en el hilo principal de asyncio."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task())
    loop.close()

# Programar el mensaje semanal (cada domingo a las 12:00)
schedule.every().sunday.at("00:00").do(lambda: ejecutar_asyncio(enviar_mensaje_semanal))

# Bucle infinito para ejecutar las tareas programadas
print("✅ Bot semanal iniciado. Esperando el horario programado...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Espera 60 segundos antes de revisar nuevamente

