## wxManager使用教程

## 1、解析数据

```python
import json
import os
from multiprocessing import freeze_support

from wxManager import Me
from wxManager.decrypt import get_info_v4, get_info_v3
from wxManager.decrypt.decrypt_dat import get_decode_code_v4
from wxManager.decrypt import decrypt_v4, decrypt_v3

if __name__ == '__main__':
    freeze_support()  # 使用多进程必须

    r_4 = get_info_v4()  # 微信4.0
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
        decrypt_v4.decrypt_db_files(key, src_dir=wx_dir, dest_dir=output_dir)
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
        decrypt_v3.decrypt_db_files(key, src_dir=wx_dir, dest_dir=output_dir)
        with open(os.path.join(output_dir, 'Msg', 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
```


## 2、查看联系人

```python
import time

from wxManager import DatabaseConnection

db_dir = ''  # 解析后的数据库路径，例如：./db_storage
db_version = 4  # 数据库版本，4 or 3

conn = DatabaseConnection(db_dir, db_version)  # 创建数据库连接
database = conn.get_interface()  # 获取数据库接口

st = time.time()
cnt = 0
contacts = database.get_contacts()
for contact in contacts:
    print(contact)
    contact.small_head_img_blog = database.get_avatar_buffer(contact.wxid)
    cnt += 1
    if contact.is_chatroom:
        print('*' * 80)
        print(contact)
        chatroom_members = database.get_chatroom_members(contact.wxid)
        print(contact.wxid, '群成员个数：', len(chatroom_members))
        for wxid, chatroom_member in chatroom_members.items():
            chatroom_member.small_head_img_blog = database.get_avatar_buffer(wxid)
            print(chatroom_member)
            cnt += 1

et = time.time()

print(f'联系人个数：{cnt} 耗时：{et - st:.2f}s')
```

## 3、导出数据

```python
import time
from multiprocessing import freeze_support

from exporter.config import FileType
from exporter import HtmlExporter, TxtExporter, AiTxtExporter, DocxExporter, MarkdownExporter, ExcelExporter
from wxManager import DatabaseConnection, MessageType


def export():
    st = time.time()

    db_dir = ''  # 解析后的数据库路径，例如：./db_storage
    db_version = 4  # 数据库版本，4 or 3

    wxid = 'wxid_00112233'  # 要导出好友的wxid
    output_dir = './data/'  # 输出文件夹

    conn = DatabaseConnection(db_dir, db_version)  # 创建数据库连接
    database = conn.get_interface()  # 获取数据库接口

    contact = database.get_contact_by_username(wxid)  # 查找某个联系人
    exporter = HtmlExporter(
        database,
        contact,
        output_dir=output_dir,
        type_=FileType.HTML,
        message_types={MessageType.MergedMessages},  # 要导出的消息类型，默认全导出
        time_range=['2020-01-01 00:00:00', '2035-03-12 00:00:00'],  # 要导出的日期范围，默认全导出
        group_members=None  # 指定导出群聊里某个或者几个群成员的聊天记录
    )

    exporter.start()
    et = time.time()
    print(f'耗时：{et - st:.2f}s')


if __name__ == '__main__':
    freeze_support()
    export()
```