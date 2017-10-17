#!/usr/bin/env python3
# coding : utf-8
import sys
import os
class Config:
    def __init__(self,configfile):
        self.configfile = configfile
        self.config = {

        }
        with open(configfile) as file:
            for line in file:
                line = line.strip()
                name = line.split("=")[0].strip()
                vule = line.split("=")[1].strip()
                self.config[name] = vule


    def get_config(self,name):
        return self.config[name]


class UserData:
    def __init__(self,userdatafile):
        self.userdata ={

        }
        with open("user.csv") as file:
            for line in file:
                line = line.strip()
                num = line.split(",")[0].strip()
                wage = line.split(",")[1].strip()
                self.userdata[num] = wage

    def calculator(self):

        def table(Taxable_Income):
            if 1500 >= Taxable_Income:
                return 0.03, 0
            elif 4500 >= Taxable_Income > 1500:
                return 0.1, 105
            elif 9000 >= Taxable_Income > 4500:
                return 0.2, 555
            elif 35000 >= Taxable_Income > 9000:
                return 0.25, 1005
            elif 55000 >= Taxable_Income > 35000:
                return 0.3, 2755
            elif 80000 >= Taxable_Income > 55000:
                return 0.35, 5505
            elif Taxable_Income > 80000:
                return 0.45, 13505

        def tax(num, wage):
            all = []

            if wage <= 0:  # 工资负数直接不计算
                print("Parameter Error")
                return
            '''
            计算税的代码和2主要区别在这里,一个最高值 一个最低值
            '''
            JiShuL = float(config.get_config("JiShuL"))
            JiShuH = float(config.get_config("JiShuH"))
            if wage < JiShuL:
                insurance = JiShuL * 0.165  # 计算社保金额
            elif wage > JiShuH:
                insurance = JiShuH * 0.165  # 计算社保金额
            else:
                insurance = wage * 0.165     # 计算社保金额

            Taxable_Income = wage - 3500 - insurance  # 应纳税额
            if Taxable_Income <= 0:  # 如果应纳税所得额为负则不需要纳税.应纳税所得额=0
                Taxable_Income = 0.00
            tax_rate, take_out = table(Taxable_Income)  # 计算税率和速扣
            Tax_payable = Taxable_Income * tax_rate - take_out   #个人所得税
            finally_wage = wage - Tax_payable - insurance        #税后工资

            # print(num + ":" + str('%.2f' % finally_wage))  # 保留两位小数
            '''工号,税前工资,社保金额,个税金额,税后工资'''
            content = "{num},{wage},{insurance:.2f},{Tax_payable:.2f},{finally_wage:.2f}".format(num=num,wage=wage,\
                                                                                 insurance=insurance,Tax_payable=Tax_payable,\
                                                                                 finally_wage=finally_wage)
            self.content += content+'\n'

        self.content = '' #输出内容 用来写入到文件
        for _ in self.userdata:
            tax(_,int(self.userdata[_]))

    def dumptofile(self, outputfile):
        with open(outputfile,'a') as file:
            file.write(self.content)


if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        configfile = args[args.index('-c')+1]
        userdata =  args[args.index('-d')+1]
        outfile = args[args.index('-o')+1]
    except:
        print("Parameter Error")
        sys.exit()

    if os.path.isfile(configfile) == False or os.path.isfile(userdata) == False:#配置文件不存在结束
        print("Parameter Error")
        sys.exit()

    config = Config(configfile)
    # # print(aaa.get_config("JiShuL"))
    bbb = UserData(userdata)
    bbb.calculator()
    bbb.dumptofile(outfile)
