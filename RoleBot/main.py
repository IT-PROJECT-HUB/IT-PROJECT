import discord  # pip install discord.py
import config

intents = discord.Intents.default()
intents.members = True


class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f"Бот {self.user} в сети!")

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.ID_POST:
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)

            try:
                role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])

                if len([i for i in user.roles if i.id not in config.USER_ROLES_LIST]) <= config.MAX_ROLES:
                    await user.add_roles(role)
                    print(f"{user.name} получил роль {role.name}")
                else:
                    await message.remove_reaction(payload.emoji, user)
                    print(f"Ошибка! пользователь {user.name} пытался получить слишком много ролей")

            except Exception as _ex:
                print(repr(_ex))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = discord.utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
            await user.remove_roles(role)
        except Exception as _ex:
            print(repr(_ex))


client = DiscordBot(intents=intents)
client.run(config.BOT_TOKEN)
