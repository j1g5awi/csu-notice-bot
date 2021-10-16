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
  **例：**`csu_notice unsub cse`（取消订阅计算机院通知）
- `csu_notice set name value`设置配置项
  - `api_server: str`API 服务器地址
  - `token: str`重载截图需要的 token
  - `limit: int`每次通知推送的数量限制
  - `enable_content: bool`通知推送时是否带截图
- `csu_notice srch title`搜索标题含有该关键字的最近五个通知
  - `-T, --tag tag`指定 tag，默认为`main`
- `csu_notice show id`返回对应通知的详细内容，不带参数则返回最新通知
  - `-T, --tag tag`指定 tag，默认为`main`
- `csu_notice rl id`重载对应通知的截图
  - `-T, --tag tag`指定 tag，默认为`main`
- `csu_notice fl`设置过滤器
  - `-f, --from from ...`来源
  - `-k, --keyword keyword ...`关键词
  - `-r, --remove`删除模式
  - `-O, --filter-out`反向过滤器  
  **例：**`csu_notice fl -O -f 采购与招标管理中心`过滤掉采购与招标中心的通知
### License

[AGPL-3.0 License](LICENSE)
