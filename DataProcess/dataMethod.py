#import MySQLdb
import numpy as np
import math
import csv
# class for the data processing

class data :

    # file path
    file_path = '/home/wanghao/Document/tianchi/data_sets'
    taobao_path = file_path + '/ijcai2016_taobao'
    merchantinfo_path = file_path + '/ijcai2016_merchant_info'
    koubeitrain_path = file_path + '/ijcai2016_koubei_train'
    koubeitest_path = file_path + '/ijcai2016_koubei_test'

    #result_path = '/home/wanghao/Document/tianchi/result/result.csv'

    merchant_budget = {}
    location_merchant = {}
    location_merchant_nums = {}
    user_merchant_nums = {}
    user = {}
    merchant ={}
    user_sim = {}
    #seller_user_nums = {}

    def __init__(self):
        print "init"

    def inputdata(self):

        print "input the data ....."

        # Process the taobao

        #file = open(self.taobao_path,'r')
        #for line in file:
        #    print line

        # process the merchant file
        file = open(self.merchantinfo_path,'r')
        for line in file:
            linelist = line.split(',')
            self.merchant_budget.setdefault(linelist[0],linelist[1])

            locationlist = linelist[2].split(':')
            for location in locationlist:
                if self.location_merchant.has_key(location):
                    self.location_merchant[location].append(linelist[0])
                else:
                    self.location_merchant[location] = [linelist[0]]

        print ("the location nums is %d"%(len(self.location_merchant)))
        print ("the merchant nums is %d"%(len(self.merchant_budget)))

        #for dict in self.location_merchant:
         #   print dict
          #  print self.location_merchant.get(dict)


        # Process the train file


        # Process the test file

    def outputdata(self):
        print "output the result to csv"

    def setdatapath(self,foldpath):

        self.file_path = foldpath

    def get_location_merchant_nums(self):
        # process train file
        with open(self.koubeitrain_path) as f:
            for line in f:
                linelist = line.split(',')
                location = linelist[2]
                merchant = linelist[1]
                if self.location_merchant_nums.has_key(location):
                    merchant_nums = self.location_merchant_nums[location]
                    if merchant_nums.has_key(merchant):
                        merchant_nums[merchant] = merchant_nums[merchant] + 1
                    else:
                        merchant_nums[merchant] = 1
                else:
                    merchant_nums = {}
                    merchant_nums[merchant] = 1
                    self.location_merchant_nums[location] = merchant_nums

        for dict in self.location_merchant_nums:
            print dict, self.location_merchant_nums[dict]
    
    def input_train_data(self):
        file = open(self.koubeitrain_path,'r')
        i = 0
        for line in file:
            linelist = line.split(',')
            self.user[linelist[0]] = i
            i = i + 1
            temp_merchant_nums = {}
            if(self.user_merchant_nums.has_key(linelist[0])):
                if(self.user_merchant_nums[linelist[0]].has_key(linelist[1])):
                    self.user_merchant_nums[linelist[0]][linelist[1]] = self.user_merchant_nums[linelist[0]][linelist[1]] + 1
                else:
                    self.user_merchant_nums[linelist[0]][linelist[1]] = 1
            else:
                temp_merchant_nums[linelist[1]] = 1
                self.user_merchant_nums[linelist[0]] = temp_merchant_nums
            #self.user_merchant = sorted(self.user_merchant.iteritems(),key = lambda d:d[0])
        print('number of user:%d'%len(self.user))
        print('number of user_merchant:%d'%len(self.user_merchant_nums))

    def input_merchant_data(self):
        file = open(self.merchantinfo_path,'r')
        j = 0
        for line in file:
            linelist1 = line.split(',')
            self.merchant[linelist1[0]] = j
            j = j + 1
        print('number of merchant:%d'%len(self.merchant))

    # user similarity
    def Mer_Sim(self,d1,d2):

        keys1 = set(d1.keys())
        keys2 = set(d2.keys())
        commonkeys = keys1 & keys2
        upper = 0.0
        for key in commonkeys:
            upper = upper + d1[key]*d2[key]
        fa = 0.0
        for key in d1.keys():
            fa = fa + d1[key]*d1[key]
        fa = math.sqrt(fa)
        fb = 0.0
        for key in d2.keys():
            fb = fb + d2[key]*d2[key]
        fb = math.sqrt(fb)

        return float(upper / (fa * fb))


    def Comp_User_Sim(self):
        count = 0
        # sort the user_merchant
        keylist = sorted(self.user_merchant_nums.iterkeys())
        keylen = len(keylist)

        user1 = keylist[0:keylen/1000]

        user2 = keylist[keylen/10 : 2*keylen/10]
        user3 = keylist[2*keylen / 10: 3 * keylen / 10]
        user4 = keylist[3*keylen / 10: 4 * keylen / 10]
        user5 = keylist[4*keylen / 10: 5 * keylen / 10]
        user6 = keylist[5*keylen / 10: 6 * keylen / 10]
        user7 = keylist[6*keylen / 10: 7 * keylen / 10]
        user8 = keylist[7*keylen / 10: 8 * keylen / 10]
        user9 = keylist[8 * keylen / 10: 9 * keylen / 10]
        user10 = keylist[9 * keylen / 10: keylen]

        for usr_i in user1:
            mer_dict_i = self.user_merchant_nums[usr_i]
            self.user_sim[usr_i] = []
            count = count + 1
            print "current count ",count
            for usr_j in self.user_merchant_nums:
                mer_dict_j = self.user_merchant_nums[usr_j]
                if self.Mer_Sim(mer_dict_i,mer_dict_j) > 0.8:
                    self.user_sim[usr_i].append(usr_j)
        result = []
        usr_count = []
        # get the result for user_sim

        print "The user_sim len ", len(self.user_sim)
        count = 0
        for usr in self.user_sim:
            res = []
            res.append(usr)
            usr_count.append(len(self.user_sim[usr]))
            string = ''
            for usrs in self.user_sim[usr]:
                string = string + str(usrs) + ':'

            string = string[0:len(string)-1]
            res.append(string)
            result.append(res)

        csvfile = '/home/wanghao/Document/tianchi/result/simi_usr1.csv'

         # print "result ......."
         #  for r in result :
         #      print r
        with open(csvfile,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(result)

        print usr_count
        usr_count.sort(reverse=True)
        print "Reverse .........."
        print usr_count

        print usr_count[0:5]


if __name__ == '__main__':
    print "hello python "
    d = data()
    #d.input_traindata()
    #  def input_taobao_data(self):
    #      file = open(self.taobao_path,'r')
    d.input_train_data()
    # d.Comp_User_Sim()
    for temp in d.user_merchant_nums:
        print temp,d.user_merchant_nums[temp]
    d.get_location_merchant_nums()
