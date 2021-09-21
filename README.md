# CSU Notice Bot

*基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，使用 [csu-notice-api](https://github.com/MagicalSheep/csu-notice-api) 的中南大学通知 QQ 机器人。*

Demo：[Dr.Sink](https://wpa.qq.com/msgrd?v=3&uin=1351483470&site=qq&menu=yes)

[![License](https://img.shields.io/github/license/j1g5awi/csu-notice-bot)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a15+-red.svg)

### Usage

- `csu_notice sub tag` 在本群订阅通知（默认为校内通知）  
  **例：**`csu_notice sub cse` （订阅计算机院通知）
- `csu_notice ubsub tag` 在本群取消订阅通知（默认为所有通知）  
  **例：**`csu_notice unsub cse` （取消订阅计算机院通知）
- `csu_notice set api_server` 设置通知 API 服务器

### License

[AGPL-3.0 License](LICENSE)
