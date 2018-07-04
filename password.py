import pickle

class passwd(object):
    rootid=0
    def __init__(self,name,url,remarks,password,way,level):
        #名字
        self.name=name
        #网站
        self.url=url
        #备注
        self.remarks=remarks
        #密码
        self.__password=password
        #加密方式
        self.__way=way
        #本密码等级
        self.__level=level
        #密码条数
        self.id=passwd.rootid
        passwd.rootid +=1
    def get_whole(self):
        print("------------------------------------------------------------------------------------------------------------------------------------------------")
        print("%-20.20s%-20.20s%-20.20s%-20.20s%-20.20s%-20.20s%-20.20s"%("id","密码名字","网站","备注","密码","加密方式","安全等级"))

        print("%-20.20s%-23.20s%-21.20s%-17.20s%-22.20s%-23.20s%-20.20s"%(self.id,self.name,self.url,self.remarks, self.__password,self.__way,self.__level))
        print("------------------------------------------------------------------------------------------------------------------------------------------------")
    def get(self,which):
        if which == "name":
            print(self.name)
        elif which=="url":
            print(self.url)
        elif which=="remarks":
            print(self.remarks)
        elif which=="password":
            print(self.__password)
        elif which=="way":
            print(self.__way)
        elif which=="url":
            print(self.__url)
        elif which== "level":
            print(self.__level)
        else :
            print("输入有误，请检查输入")

    def change(self,which,data):
        if which == "name":
            self.name=data
        elif which=="url":
            self.url=data
        elif which=="remarks":
            self.remarks=data
        elif which=="password":
            self.__password=data
        elif which=="way":
            self.__way=data
        elif which=="url":
            self.__url=data
        elif which== "level":
            self.__level=data
        else :
            print("输入有误，请检查输入")

    def get_dict(self):
        return {"id":self.id,"name":self.name,"url":self.url,"remarks":self.remarks, "password":self.__password,"way":self.__way,"level":self.__level}

class menu(object):
    switch = """
_______________________________________________
1.修改
2.添加
3.获得密码
4.保存修改
5.查看
6.删除
其他：查看名字列表
_______________________________________________
    """
    def __init__(self,name):
        self.__name=menu
    def get_menu(self):
        print(self.switch)

def read_data():
    with open("data.pkl",'rb') as pickle_file:
        return pickle.load(pickle_file)
def write_data(dict_data):
    with open("data.pkl",'wb') as pickle_file:
        pickle.dump(dict_data,pickle_file)

def main():

    #print("first input you root password :")
    #rootpwd=input()
    dict_data = read_data()
    passwd.rootid=dict_data[id]
    while True:
        print(menu.switch)
        choice=input()
        if choice == "1":
            pwd1,switch1,data1=input("输入修改的属性，和内容:").split(" ")
            dict_data[pwd1].change(switch1,data1)
        elif choice == "2":
            pwd_name,url2,remarks2,password2,way2,level2=input("输入密码名字 网站 备注 密码 加密方式 安全等级:\n").split(" ")
            dict_data[pwd_name]=passwd(pwd_name,url2,remarks2,password2,way2,level2)
        elif choice=="3":
            chaxun_pwd_name=input("输入要查询的名字:")
            dict_data[chaxun_pwd_name].get("password")
        elif choice == "4":
            print(dict_data)
            dict_data[id]=passwd.rootid
            write_data(dict_data)
            dict_data = read_data()
        elif choice == "5":
            look_pwd_name=input("输入需要查看的条目名字：")
            print(dict_data[look_pwd_name].get_whole())
        elif choice == "6":
            del_name=input("输入你要删除的名字:")
            dict_data.pop(del_name)
        else:
            for x in dict_data.keys():
                print(x,' ',end='')
def init():
    #初次运行把passwd.rootid=dict_data[id] 注释掉
    dict_data={}
    write_data({"pwd":passwd("pwdddddddd1","www.baidu.com","百度网站密码","1234","lol",7),
"pwd2":passwd("pd2", "www.bagcom", "55网站密码", "1sg34", "ladfl", 7),
"pwd3":passwd("pwd31", "www.badadu.com", "sd网站密码", "12asf34", "laal", 7)})
    
    pwd_name,url2,remarks2,password2,way2,level2=input("输入密码名字 网站 备注 密码 加密方式 安全等级:\n").split(" ")
    dict_data[pwd_name]=passwd(pwd_name,url2,remarks2,password2,way2,level2)
    dict_data[id]=passwd.rootid
    write_data(dict_data)
if __name__ == '__main__':
    main()
    #init()