import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

GUILD_ID = 780272199248248852

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"✅ Bot conectado como {bot.user}")

class CartaButton(Button):
    def __init__(self, label, color):
        super().__init__(label=label, style=color)
        self.original_style = color
        self.emoji_char = label[0]  # Guardamos el emoji para mantenerlo

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.view.owner:
            await interaction.response.send_message(
                "❌ Este tablero no es tuyo.", ephemeral=True
            )
            return
        self.style = discord.ButtonStyle.secondary  # se pone gris
        self.label = str(self.emoji_char) + self.label[1:]  # mantener emoji
        await interaction.response.edit_message(view=self.view)

class CartasView(View):
    def __init__(self, owner):
        super().__init__(timeout=None)
        self.owner = owner

        # Definir colores y emojis
        colores = [
            ("🟡", discord.ButtonStyle.success),  # Amarillo simulado con fondo verde
            ("🔴", discord.ButtonStyle.danger),   # Rojo
            ("🔵", discord.ButtonStyle.primary)   # Azul
        ]

        for emoji, color in colores:
            for i in range(8):
                button = CartaButton(label=f"{emoji}{i+1}", color=color)
                self.add_item(button)

        # Botón Reset
        reset_button = Button(label="Reset", style=discord.ButtonStyle.secondary)
        async def reset_callback(interaction: discord.Interaction):
            if interaction.user != self.owner:
                await interaction.response.send_message(
                    "❌ Este tablero no es tuyo.", ephemeral=True
                )
                return
            for item in self.children:
                if isinstance(item, CartaButton):
                    item.style = item.original_style
                    item.label = str(item.emoji_char) + item.label[1:]
            await interaction.response.edit_message(view=self)
        reset_button.callback = reset_callback
        self.add_item(reset_button)

@bot.tree.command(name="cartas", description="Muestra tu tablero de cartas privado")
async def cartas(interaction: discord.Interaction):
    view = CartasView(owner=interaction.user)
    await interaction.response.send_message(
        "Tu tablero de cartas:", view=view, ephemeral=True
    )

    # Botón Ver puntos
    view_puntos = View(timeout=None)
    puntos_button = Button(label="Ver puntos", style=discord.ButtonStyle.primary)
    async def puntos_callback(interaction2: discord.Interaction):
        if interaction2.user != interaction.user:
            await interaction2.response.send_message(
                "❌ Este tablero no es tuyo.", ephemeral=True
            )
            return
        await interaction2.response.send_message(
            "📌 Referencia de puntos:",
            ephemeral=True,
            file=discord.File("C:/Users/USER/Desktop/Okey helper/Referencia.png")
        )
    puntos_button.callback = puntos_callback
    view_puntos.add_item(puntos_button)
    await interaction.followup.send("Referencia de puntos:", view=view_puntos, ephemeral=True)

# === NUNCA PONGAS EL TOKEN DIRECTAMENTE EN EL CÓDIGO ===
# Mejor usamos una variable de entorno

import os
from dotenv import load_dotenv

# Intenta cargar el token desde un archivo .env (para desarrollo local)
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN') # Busca la variable DISCORD_TOKEN

if TOKEN is None:
    print("❌ ERROR: No se encontró el token. Crea un archivo .env con DISCORD_TOKEN=tu_token")
else:
    bot.run(TOKEN)
