#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2025/3/11 18:17 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : WeChatMsg-1-decrypt.py 
@Description : 
"""

import json
import os
from multiprocessing import freeze_support

from wxManager import Me
from wxManager.decrypt import get_info_v4, get_info_v3
from wxManager.decrypt.decrypt_dat import get_decode_code_v4
from wxManager.decrypt.decrypt_v4 import decrypt_db_files

if __name__ == '__main__':
    freeze_support()  # 使用多进程必须

    # r_4 = get_info_v4()  # 微信4.0
    r_4 = []
    for wx_info in r_4:
        print(wx_info)
        me = Me()
        me.wx_dir = wx_info.wx_dir
        me.wxid = wx_info.wxid
        me.name = wx_info.nick_name
        me.xor_key = get_decode_code_v4(wx_info.wx_dir)
        info_data = me.to_json()
        output_dir = wx_info.wxid
        key = wx_info.key
        wx_dir = wx_info.wx_dir
        decrypt_db_files(key, src_dir=wx_dir, dest_dir=output_dir)
        with open(os.path.join(output_dir, 'db_storage', 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)

    version_list_path = '../wxManager/decrypt/version_list.json'
    with open(version_list_path, "r", encoding="utf-8") as f:
        version_list = json.loads(f.read())
    r_3 = get_info_v3(version_list)  # 微信3.x
    for wx_info in r_3:
        print(wx_info)
        me = Me()
        me.wx_dir = wx_info.wx_dir
        me.wxid = wx_info.wxid
        me.name = wx_info.nick_name
        info_data = me.to_json()
        output_dir = wx_info.wxid
        key = wx_info.key
        wx_dir = wx_info.wx_dir
        # decrypt_db_files(key, src_dir=wx_dir, dest_dir=output_dir)
        with open(os.path.join(output_dir, 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)