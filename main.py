import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('cog').setLevel(logging.NOTSET)
    logging.getLogger('bot').setLevel(logging.NOTSET)

    log = logging.getLogger()
    log.setLevel(logging.NOTSET)
    fh = RotatingFileHandler(
        filename='log/potato_exec.log',
        encoding='utf-8',
        mode='w',
        maxBytes=32 * 1024 * 1024,
        backupCount=7
        )
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    fmt = logging.Formatter('{asctime};{name};{levelname};{message}', style='{')
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(sh)


def main():
    setup_logger()
    from bot import Bot
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
