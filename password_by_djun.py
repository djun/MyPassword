# coding=utf-8

"""
2018-6-29 created.by DJun.
"""


import pickle
# import traceback as tb


class Password:
    """
    密码项类，用于储存单个密码项
    """
    
    PROP_KEY_LIST = ['name', 'user', 'pwd', 'url', 'remarks', 'encrypt_method', 'encrypt_level']  # 与属性名称对应，用于操作属性
    PROP_NAME_LIST = ['名称', '用户名', '密码', '网址URL', '备注', '加密方式', '加密级别']  # 与上述属性名对应中文释义，用于提示文字
    
    def __init__(self):
        # 以下是必要的初始化
        self.name = 'pwd'  # 密码项名称
        self.user = None  # 用户名
        self.pwd = None  # 密码
        self.url = None  # 网址URL
        self.remarks = None  # 备注
        self.encrypt_method = None  # 加密方式
        self.encrypt_level = None  # 加密级别


class PasswordGroup:
    """
    密码集类，用于储存和管理密码集
    """
    
    DATA_FILE_NAME = 'data.pkl'  # 默认数据文件名
    
    def __init__(self):
        self._pwd_list = []  # 列表用于储存密码项
        self._pwd_dict = {}  # 字典用于快速查询密码
    
    @property
    def pwd_list(self):
        # 这里写成属性方法并使用list构造方法是为了保护self._pwd_list不受非正常方式修改
        return list(self._pwd_list)
    
    def get_pwd(self, name):
        # 通过密码名称获取密码项对象
        return self._pwd_dict.get(name)
    
    def set_pwd(self, name, key, value):
        # 通过密码名称、属性名称修改密码项中的信息
        pwd = self.get_pwd(name)
        if pwd and key in Password.PROP_KEY_LIST:
            setattr(pwd, key, value)
    
    def add(self, pwd):
        # 新增密码项
        if pwd.name not in self._pwd_dict:
            self._pwd_list.append(pwd)
            self._pwd_dict[pwd.name] = pwd
    
    def remove(self, pwd):
        # 删除密码项
        if pwd.name in self._pwd_dict:
            self._pwd_list.remove(pwd)
            self._pwd_dict.pop(pwd.name)
    
    def clear(self):
        # 清空密码集
        self._pwd_list.clear()
        self._pwd_list.clear()
    
    def rename(self, pwd, new_name):
        # 密码项改名
        if pwd.name in self._pwd_dict and new_name not in self._pwd_dict:
            self._pwd_dict.pop(pwd.name)
            pwd.name = new_name
            self._pwd_dict[pwd.name] = pwd

    def load_from_file(self, file_name=DATA_FILE_NAME):
        # 从文件读取数据
        with open(file_name, 'rb') as fp:
            obj = pickle.load(fp)
            if isinstance(obj, list):
                self.clear()
                for i in obj:
                    # 注：这里仅用密码集自带操作方法，保证对密码集操作的一致性
                    self.add(i)

    def save_to_file(self, file_name=DATA_FILE_NAME):
        # 写入数据到文件
        with open(file_name, 'wb') as fp:
             pickle.dump(self._pwd_list, fp)


class PasswordApp:
    """
    密码应用类，用于用户交互
    """
    
    def __init__(self):
        self._pwd_group = PasswordGroup()
        try:
            # 对读入数据作异常处理，无数据文件时也能正常运行
            self._pwd_group.load_from_file()
        except:
            pass
    
    def print_pwd(self, pwd_item):
        # 输出单个密码项信息内容
        if isinstance(pwd_item, Password):
            print('------{}------'.format(pwd_item.name))
            print('网址URL：{}'.format(pwd_item.url))
            print('用户名：{}\t密码：{}'.format(pwd_item.user, pwd_item.pwd))
            print('备注：{}'.format(pwd_item.remarks))
            print('加密方式：{}\t加密级别：{}'.format(pwd_item.encrypt_method, pwd_item.encrypt_level))
            print('------{}------'.format('-'*len(pwd_item.name) if pwd_item.name else ''))
    
    def cmd_add(self):
        # 命令：新增
        data_in = input('请输入数据，以空格间隔（名称 用户名 密码 网址URL 备注 加密方式 加密级别）：')
        try:
            # 采用原先代码的方式，用空格间隔来分割输入的数据
            data_in = data_in.split(' ')
            pwd_item = Password()
            # 采用“序列解包”对密码项存入数据，在此具体应用下相比利用密码项的构造方法（__init__）初始化数据来说更灵活方便
            pwd_item.name, pwd_item.user, pwd_item.pwd, pwd_item.url, pwd_item.remarks, pwd_item.encrypt_method, pwd_item.encrypt_level = data_in
            
            print('\n您刚录入的密码信息如下：')
            self.print_pwd(pwd_item)
            
            # 密码集操作（新增），保存数据到文件
            self._pwd_group.add(pwd_item)
            self._pwd_group.save_to_file()
            print('\n密码信息已录入。')
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_search(self):
        # 命令：查找
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
        # 命令：修改
        data_in = input('请输入需要操作修改的密码名称：')
        try:
            pwd_item = self._pwd_group.get_pwd(data_in)
            if not pwd_item:
                print('查询不到名称为“{}”的密码信息。'.format(data_in))
                return

            print('该密码当前信息如下：')
            self.print_pwd(pwd_item)
            
            # 构造修改操作的输入提示文字
            hint = '\t'.join('{}-{}'.format(ni+1, i) for ni, i in enumerate(Password.PROP_NAME_LIST))
            hint = '\n现有项目编号：\n' + hint + '\n0-返回上一菜单\n请输入要修改的项目编号：'
            while True:
                try:
                    item_index = input(hint)
                    item_index = item_index.strip()
                    
                    if item_index == '0':
                        # 处理“返回”操作
                        print('即将返回...')
                        break
                    # 由于将“返回”操作设定为“0”，而列表索引也从0开始，所以取属性名称、对应释义时要先作一下转换
                    item_index = int(item_index) - 1
                    item_key = Password.PROP_KEY_LIST[item_index]
                    item_name = Password.PROP_NAME_LIST[item_index]
                    
                    original_value = getattr(pwd_item, item_key)
                    new_value = input('请为项目“{}”输入新的内容（原为“{}”）：'.format(item_name, original_value))
                    if item_index == 0 and original_value != new_value:
                        # 改名操作较特殊（涉及字典处理），使用单独的方法处理
                        self._pwd_group.rename(pwd_item, new_value)
                    else:
                        # 接收到新值后直接存入密码项中，密码项的引用还在密码集中，故不用进行其他额外操作
                        setattr(pwd_item, item_key, new_value)
                    
                    # 密码集操作（修改），保存数据到文件
                    self._pwd_group.save_to_file()
                    print('\n密码信息已修改。')
                except:
                    print('输入有误，请重新输入！')
                    # print("------Traceback------\n" + tb.format_exc())
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_delete(self):
        # 命令：删除
        data_in = input('请输入需要操作删除的密码名称：')
        try:
            pwd_item = self._pwd_group.get_pwd(data_in)
            if pwd_item:
                self.print_pwd(pwd_item)
                confirm = input('确定要删除这条密码信息吗？确认请输入大写字母Y，其他则取消：')
                if confirm == 'Y':
                    # 密码集操作（删除），保存数据到文件
                    self._pwd_group.remove(pwd_item)
                    self._pwd_group.save_to_file()
                    print('\n密码信息已删除。')
                else:
                    print('\n未确认删除，即将返回...')
            else:
                print('查询不到名称为“{}”的密码信息。'.format(data_in))
        except:
            print('输入内容有误！即将返回...')
            # print("------Traceback------\n" + tb.format_exc())
    
    def cmd_list_all(self):
        # 命令：查看所有
        pwd_list = self._pwd_group.pwd_list
        if len(pwd_list) > 0:
            print('您查看的密码信息清单如下：')
            for i in pwd_list:
                self.print_pwd(i)
        else:
            print('（密码信息清单为空，请新增记录）')
    
    def run(self):
        # 利用字典，将对应输入选项映射到实际命令操作方法上
        cmd_func_map = {
            '1': self.cmd_add,
            '2': self.cmd_search,
            '3': self.cmd_modify,
            '4': self.cmd_delete,
            '5': self.cmd_list_all
        }
        cmd_selections = {str(i) for i in range(1, 6)}  # 用于限制输入范围
        
        # 与用户交互过程
        while True:
            cmd = input('\n  --------\n  1、新增\n  2、查找\n  3、修改\n  4、删除\n  5、查看所有\n\n  0、退出\n  --------\n\n请选择：')
            cmd = cmd.strip()  # 对输入的命令作裁剪，增加容错性

            print()  # 空行显得美观
            if cmd == '0':
                # 显示退出提示文字，用break跳出无限循环即可完成退出操作
                print('\n好的，即将退出...')
                break
            elif cmd in cmd_selections:
                # 使用带有映射信息的字典查找对应的命令操作方法，并执行它
                cmd_func = cmd_func_map.get(cmd)
                cmd_func()
            else:
                print('输入有误，请重新输入！')


if __name__ == '__main__':
    app = PasswordApp()
    app.run()
