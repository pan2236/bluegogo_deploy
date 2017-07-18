#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import sys
from host import Host
from business import Business
class BusinessDeploy(object):

    def __init__(self):
        self.deploy_type,self.business = sys.argv[1],sys.argv[2]
        self.deploy_type_list = self.fetch_deploy_type()
        self.business_obj = Business(self.deploy_type,self.business)
        self.business_list = self.business_obj.fetch_business_list()
        self.argv_parser()
        self.host_obj = Host(self.business,self.deploy_type)
        self.deploy_host_list = self.host_obj.deploy_host_dict.keys()
        print self.deploy_host_list
        self.business_deploy()

    #参数验证
    def argv_parser(self):
        if len(sys.argv) != 3:
            sys.exit("\033[31;1mWrong number of parameters\033[0m")
        if self.deploy_type not in self.deploy_type_list:
            print("\033[31;1mWrong of parameters,deploy type does not exist\033[0m")
            sys.exit("\033[31;1mPlease choose deploy type %s \033[0m" % self.deploy_type_list)
        if self.business not in self.business_list:
            print ("\033[31;1mWrong of parameters,business does not exist\033[0m")
            sys.exit("\033[31;1mPlease choose business %s \033[0m" % self.business_list)


    #获取所有发布方法的列表
    def fetch_deploy_type(self):
        from config import deploy_type
        return deploy_type

    #执行发布操作
    def business_deploy(self):
        try:
            if hasattr(self.business_obj,"%s_%s_before_set" %(self.business,self.deploy_type)):
                settings_before_deployment = getattr(self.business_obj,"%s_%s_before" %(self.business,self.deploy_type))
                before_ret = settings_before_deployment()

            self.deploy()

            if hasattr(self.business_obj,"%s_%s_after_set" %(self.business,self.deploy_type)):
                settings_after_deployment = getattr(self.business_obj,"%s_%s_after_set" %(self.business,self.deploy_type))
                after_ret = settings_after_deployment()
        except Exception as er:
            print er


    def deploy(self):
        from config import online_interval_num
        x, y = len(self.deploy_host_list).__divmod__(online_interval_num)
        if y != 0:
            x += 1
        for i in range(x):
            host_list = self.deploy_host_list[i * online_interval_num:(i + 1) * online_interval_num]
            print host_list
            target_expr = self.host_obj.host_expr_generate(self.host_obj.deploy_host_dict.keys())
            deploy_ret = self.host_obj.salt_obj.cmd(target_expr, "state.sls",["%s.%s" % (self.deploy_type, self.business)], expr_form='compound')
        return deploy_ret
