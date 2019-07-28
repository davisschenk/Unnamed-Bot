from utils.bot import UnnamedBot
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    bot = UnnamedBot(command_prefix='%')
    bot.run(load_all=True)


