# coding=utf-8

"""
2018-6-29 created.by DJun.
"""


import pickle
# import traceback as tb


class Password:
    PROP_KEY_LIST = ['name', 'user', 'pwd', 'url', 'remarks', 'encrypt_method', 'encrypt_level']
    PROP_NAME_LIST = ['名称', '用户名', '密码', '网址URL', '备注', '加密方式', '加密级别']
    
    def __init__(self):
        self.name = 'pwd'  # 密码项名称
        self.user = None  # 用户名
        self.pwd = None  # 密码
        self.url = None  # 网址URL
        self.remarks = None# 备注
        self.encrypt_method = None  # 加密方式
        self.encrypt_level = None  # 加密级别


class PasswordGroup:
    DATA_FILE_NAME = 'data.pkl'
    
    def __init__(self):
        self._pwd_list = []
        self._pwd_dict = {}
    
    @property
    def pwd_list(self):
        return list(self._pwd_list)
    
    def get_pwd(self, name):
        return self._pwd_dict.get(name)
    
    def set_pwd(self, name, key, value):
        pwd = self.get_pwd(name)
        if pwd and key in Password.PROP_KEY_LIST:
            setattr(pwd, key, value)
    
    def add(self, pwd):
        if pwd.name not in self._pwd_dict:
            self._pwd_list.append(pwd)
            self._pwd_dict[pwd.name] = pwd
    
    def remove(self, pwd):
        if pwd.name in self._pwd_dict:
            self._pwd_list.remove(pwd)
            self._pwd_dict.pop(pwd.name)
    
    def clear(self):
        self._pwd_list.clear()
        self._pwd_list.clear()

    def load_from_file(self, file_name=DATA_FILE_NAME):
        with open(file_name, 'rb') as fp:
            obj = pickle.load(fp)
            if isinstance(obj, list):
                self.clear()
                for i in obj:
                    self.add(i)

    def save_to_file(self, file_name=DATA_FILE_NAME):
        with open(file_name, 'wb') as fp:
             pickle.dump(self._pwd_list, fp)


class PasswordApp:
    def __init__(self):
        self._pwd_group = PasswordGroup()
        try:
            self._pwd_group.load_from_file()
        except:
            pass
    
    def print_pwd(self, pwd_item):
        if isinstance(pwd_item, Password):
            print('------{}------'.format(pwd_item.name))
            print('网址URL：{}'.format(pwd_item.url))
            print('用户名：{}\t密码：{}'.format(pwd_item.user, pwd_item.pwd))
            print('备注：{}'.format(pwd_item.remarks))
            print('加密方式：{}\t加密级别：{}'.format(pwd_item.encrypt_method, pwd_item.encrypt_level))
            print('------{}------'.format('-'*len(pwd_item.name) if pwd_item.name else ''))
    
    def cmd_add(self):
        data_in = input('请输入数据，以空格间隔（名称 用户名 密码 网址URL 备注 加密方式 加密级别）：')
        try:
            data_in = data_in.split(' ')
            pwd_item = Password()
            pwd_item.name, pwd_item.user, pwd_item.pwd, pwd_item.url, pwd_item.remarks, pwd_item.encrypt_method, pwd_item.encrypt_level = data_in
            print('\n您刚录入的密码信息如下：')
            self.print_pwd(pwd_item)
            self._pwd_group.add(pwd_item)
            self._pwd_group.save_to_file()
            print('\n密码信息已录入。')
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_search(self):
        data_in = input('请输入查询的密码名称：')
        try:
            pwd_item = self._pwd_group.get_pwd(data_in)
            if pwd_item:
                print('您查询的密码信息如下：')
                self.print_pwd(pwd_item)
            else:
                print('查询不到名称为“{}”的密码信息。'.format(data_in))
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_modify(self):
        data_in = input('请输入需要操作修改的密码名称：')
        try:
            pwd_item = self._pwd_group.get_pwd(data_in)
            if not pwd_item:
                print('查询不到名称为“{}”的密码信息。'.format(data_in))
                return

            print('该密码当前信息如下：')
            self.print_pwd(pwd_item)
            
            hint = '\t'.join('{}-{}'.format(ni+1, i) for ni, i in enumerate(Password.PROP_NAME_LIST))
            hint = '\n现有项目编号：\n' + hint + '\n0-返回上一菜单\n请输入要修改的项目编号：'
            while True:
                try:
                    item_index = input(hint)
                    item_index = item_index.strip()
                    if item_index == '0':
                        print('即将返回...')
                        break
                    item_index = int(item_index) - 1
                    item_name = Password.PROP_NAME_LIST[item_index]
                    item_key = Password.PROP_KEY_LIST[item_index]
                    value = input('请为项目“{}”输入新的内容：'.format(item_name))
                    setattr(pwd_item, item_key, value)
                    self._pwd_group.save_to_file()
                    print('\n密码信息已修改。')
                except:
                    print('输入有误，请重新输入！')
                    # print("------Traceback------\n" + tb.format_exc())
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_delete(self):
        data_in = input('请输入需要操作删除的密码名称：')
        try:
            pwd_item = self._pwd_group.get_pwd(data_in)
            self.print_pwd(pwd_item)
            confirm = input('确定要删除这条密码信息吗？确认请输入大写字母Y，其他则取消：')
            if confirm == 'Y':
                self._pwd_group.remove(pwd_item)
                self._pwd_group.save_to_file()
                print('\n密码信息已删除。')
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_list_all(self):
        pwd_list = self._pwd_group.pwd_list
        if len(pwd_list) > 0:
            print('您查看的密码信息清单如下：')
            for i in pwd_list:
                self.print_pwd(i)
        else:
            print('（密码信息清单为空，请新增记录）')
    
    def run(self):
        cmd_func_map = {
            '1': self.cmd_add,
            '2': self.cmd_search,
            '3': self.cmd_modify,
            '4': self.cmd_delete,
            '5': self.cmd_list_all
        }
        cmd_selections = {str(i) for i in range(1, 6)}
        
        while True:
            cmd = input('\n  --------\n  1、新增\n  2、查找\n  3、修改\n  4、删除\n  5、查看所有\n\n  0、退出\n  --------\n\n请选择：')
            cmd = cmd.strip()

            print()
            if cmd == '0':
                print('\n好的，即将退出...')
                break
            elif cmd in cmd_selections:
                cmd_func = cmd_func_map.get(cmd)
                cmd_func()
            else:
                print('输入有误，请重新输入！')


if __name__ == '__main__':
    app = PasswordApp()
    app.run()
