## wxManager使用教程

### 1、解析数据

```python
import json
import os
import time
from multiprocessing import freeze_support

import pymem

from wxManager import Me
from wxManager.decrypt import get_wx_info
from wxManager.decrypt.decrypt_dat import get_decode_code_v4
from wxManager.decrypt.wxinfo import dump_wechat_info_v4_
from wxManager.decrypt.decrypt import decrypt_db_files


def dump_v4():
    freeze_support()
    st = time.time()
    pm = pymem.Pymem("Weixin.exe")
    pid = pm.process_id
    w = dump_wechat_info_v4_(pid)
    if w:
        print(w)
        et = time.time()
        print(et - st)
        me = Me()
        me.wx_dir = w.wx_dir
        me.wxid = w.wxid
        me.name = w.nick_name
        me.xor_key = get_decode_code_v4(w.wx_dir)
        info_data = me.to_json()
        output_dir = w.wxid
        key = w.key
        wx_dir = w.wx_dir
        decrypt_db_files(key, src_dir=wx_dir, dest_dir=output_dir)
        with open(os.path.join(output_dir, 'db_storage', 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
    else:
        print('数据解析失败')


def dump_v3():
    version__list_path = '../../wxManager/decrypt/version_list.json'
    with open(version__list_path, "r", encoding="utf-8") as f:
        version__list = json.loads(f.read())
    wx_info_v3 = get_wx_info.get_info_v3(version__list)

    for wx_info in wx_info_v3:
        errcode = wx_info.get('errcode')
        if errcode == 405:
            print(wx_info.get('errmsg'))
        elif errcode == 200:
            print(wx_info)


if __name__ == '__main__':
    dump_v4()
    # dump_v3()
```

### 2、导出聊天记录

#### 查看联系人

```python
from wxManager import DatabaseConnection

db_dir = '' # 数据库路径
conn = DatabaseConnection(db_dir, db_version=4)
database = conn.get_interface()

contacts = database.get_contacts()
for contact in contacts:
    contact.smallHeadImgBLOG = database.get_avatar_buffer(contact.wxid) # 头像
    if contact.is_chatroom:
        print('*' * 80)
        print(contact)
        chatroom_members = database.get_chatroom_members(contact.wxid)
        print('群成员个数：', len(chatroom_members))
        for wxid, chatroom_member in chatroom_members.items():
            chatroom_member.smallHeadImgBLOG = database.get_avatar_buffer(wxid)
            print(chatroom_member)
```

#### 导出TXT

```python
from exporter.config import FileType
from exporter.exporter_txt import TxtExporter
from wxManager import DatabaseConnection


db_dir = '' # 数据库路径
wxid = '' # 要导出联系人的wxid
output_dir = './data/' # 输出文件夹

conn = DatabaseConnection(db_dir, db_version=4)
database = conn.get_interface()

contact = database.get_contact_by_username(wxid)

exporter = TxtExporter(
    database,
    contact,
    output_dir=output_dir,
    type_=FileType.TXT,
    message_types=None,
    time_range=None,
    group_members=None
)


# 设置自定义进度回调函数
def update_progress(progress):
    print(progress)


exporter.set_update_callback(update_progress)
exporter.start()
```

#### 导出Excel

```python
from multiprocessing import freeze_support

from exporter.config import FileType
from exporter.exporter_xlsx import ExcelExporter
from wxManager import DatabaseConnection

if __name__ == '__main__':
    freeze_support()
    db_dir = ''  # 解析后的数据库文件夹
    wxid = 'xxx'
    output_dir = './data/'
    conn = DatabaseConnection(db_dir, db_version=4)
    database = conn.get_interface()
    contact = database.get_contact_by_username(wxid)
    exporter = ExcelExporter(
        database,
        contact,
        output_dir=output_dir,
        type_=FileType.XLSX,
        message_types=None,
        time_range=None,
        group_members=None
    )
    def update_progress(progress):
        print(progress)
    # exporter.set_update_callback(update_progress)
    exporter.start()
```

#### 导出HTML

```python
import time
from multiprocessing import freeze_support

from exporter.config import FileType
from exporter.exporter_html import HtmlExporterBase
from wxManager import DatabaseConnection

if __name__ == '__main__':
    freeze_support()
    st = time.time()

    db_dir = ''  # 解析后的数据库文件夹
    wxid = ''  # 要导出好友的wxid
    output_dir = './data/'  # 输出文件夹

    conn = DatabaseConnection(db_dir, db_version=4)
    database = conn.get_interface()
    contact = database.get_contact_by_username(wxid)

    exporter = HtmlExporterBase(
        database,
        contact,
        output_dir=output_dir,
        type_=FileType.TXT,
        message_types=None,
        time_range=None,
        group_members=None
    )


    def update_progress(progress):
        print(progress)
    exporter.set_update_callback(update_progress)
    exporter.start()
    et = time.time()
    print(f'耗时：{et - st:.2f}s')
```