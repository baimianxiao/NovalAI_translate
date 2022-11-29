# -*- encoding:utf-8 -*-
import json

config = {}  # 初始化设置列表

config_path = ""

config = json.loads(config_path)  # 读取设置文件


# 获取设置
def get_config(key, sub_key):
    if key in config and sub_key in config[key]:
        return config[key][sub_key]
    return None
