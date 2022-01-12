import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init()

app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

nonebot.load_plugin("csu_notice")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
