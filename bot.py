import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()

app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_plugin("csu_notice")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
