import util
import telethon.events
import telethon

log = util.get_log("main")
log.info("AlterPy")

telethon_config = util.get_config("telethon_config.toml")
api_id = telethon_config['api_id']
api_hash = telethon_config['api_hash']
bot_token = telethon_config['bot_token']
client = telethon.TelegramClient("alterpy", api_id, api_hash)
client.start(bot_token=bot_token)
log.info("Started telethon instance")

# load all CommandHandlers from external files

@client.on(telethon.events.NewMessage)
async def event_handler(event):
    pass