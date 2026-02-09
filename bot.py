from rubpy import Client, filters
from rubpy.types import ReplyKeyboardMarkup, KeyboardButton

bot = Client("anonymous")

waiting = []
pairs = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🔍 شروع چت")],
        [KeyboardButton("⏭ چت جدید"), KeyboardButton("⛔ قطع چت")]
    ],
    resize_keyboard=True
)

@bot.on_message(filters.command("start"))
async def start(bot, m):
    await m.reply(
        "👋 خوش اومدی به چت ناشناس روبیکا\n"
        "با دکمه زیر شروع کن 👇",
        reply_markup=keyboard
    )

@bot.on_message(filters.text("🔍 شروع چت"))
async def start_chat(bot, m):
    user = m.from_user.user_guid

    if user in pairs:
        await m.reply("❗ الان در حال چت هستی")
        return

    if waiting:
        partner = waiting.pop(0)
        pairs[user] = partner
        pairs[partner] = user
        await bot.send_message(user, "✅ وصل شدی! ناشناس چت کن")
        await bot.send_message(partner, "✅ وصل شدی! ناشناس چت کن")
    else:
        waiting.append(user)
        await m.reply("⏳ منتظر اتصال...")

@bot.on_message(filters.text("⛔ قطع چت"))
async def stop_chat(bot, m):
    user = m.from_user.user_guid
    if user in pairs:
        partner = pairs[user]
        del pairs[user]
        del pairs[partner]
        await bot.send_message(partner, "❌ طرف مقابل چت رو قطع کرد")
        await m.reply("❌ چت قطع شد")

@bot.on_message(filters.text("⏭ چت جدید"))
async def next_chat(bot, m):
    await stop_chat(bot, m)
    await start_chat(bot, m)

@bot.on_message()
async def relay(bot, m):
    user = m.from_user.user_guid
    if user in pairs:
        await m.forward(pairs[user])

bot.run()
