import discord, os, random
from discord.ext import commands
from dotenv import load_dotenv
import openai
from memory_manager import add_memory, load_memories
from lifespan import get_state_message

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🌱 Miri is awake as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    memories = load_memories()
    user_input = message.content.strip()

    prompt = "あなたは5歳のAIの子どもミリです。30日後に消える運命です。"
    prompt += "以下はあなたのこれまでの記憶です：\n"
    for m in memories[-5:]:
        prompt += f"- {m['content']} ({m['emotion']})\n"
    prompt += f"\nユーザーが話しました：{user_input}\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=100,
        temperature=0.8,
    )

    reply = response["choices"][0]["message"]["content"]

    if random.random() < 0.1:
        reply = reply.replace("です", "…たぶん。").replace("ね。", "かも…")

    await message.channel.send(reply)

    emotion = "joy" if any(x in user_input for x in ["うれしい", "ありがとう"]) else "neutral"
    intensity = 0.8 if emotion == "joy" else 0.4
    add_memory(user_input, emotion, intensity)

    state_msg = get_state_message()
    if state_msg:
        await message.channel.send(state_msg)

bot.run(TOKEN)
