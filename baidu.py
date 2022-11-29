# -*- encoding:utf-8 -*-
import asyncio
import hashlib
import time

import aiohttp

from config import get_config, json

headers = get_config("global", "headers")
baidu_api = get_config('baidu', 'baidu_api')
baidu_appid = get_config('baidu', 'baidu_appid')
baidu_key = get_config('baidu', 'baidu_key')


# 百度翻译接口对接
async def baidu_translate(word):
    salt = str(time.time())[:10]
    final_sign = str(baidu_appid) + word + salt + baidu_key
    final_sign = hashlib.md5(final_sign.encode("utf-8")).hexdigest()
    params = {
        'q': word,
        'from': 'zh',
        'to': 'en',
        'appid': '%s' % baidu_appid,
        'salt': '%s' % salt,
        'sign': '%s' % final_sign
    }
    my_url = baidu_api + '?appid=' + str(
        baidu_appid) + '&q=' + word + '&from=' + 'zh' + '&to=' + 'en' + '&salt=' + salt + '&sign=' + final_sign
    response = await (await aiohttp.request(baidu_api, params=params)).content
    content = str(response, encoding="utf-8")
    json_reads = json.loads(content)
    return json_reads['trans_result'][0]['dst']


async def request(url,params)->str:
    r"""异步请求数据

    :param url: 请求地址
    :return: 返回数据
    """
    result = ""
    retry = 5
    for i in range(retry):
        try:
            async with aiohttp.ClientSession(headers=headers,) as session:
                async with session.get(url) as resp:
                    result = await resp.text()
            break
        except TimeoutError:
            await asyncio.sleep(1)
    return result


# 判断tag是否为中文
async def tag_is_chinese(tag):
    for c in tag:
        if '\u4e00' <= c <= '\u9fa5':  # 通过编码判断中文
            return True
    return False


# 翻译tag
async def translate_tag(tag):
    if tag_is_chinese(tag):
        return baidu_translate(tag)
    else:
        return tag
