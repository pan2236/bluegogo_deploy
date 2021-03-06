#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import sys,os
import subprocess
from config import nginx_config
from host import Host
import salt.client

#业务配置类
class Business(object):

    def __init__(self,deploy_type,business):
        self.business = business
        self.deploy_type = deploy_type
        # self.host_obj = Host(business,business)
        self.salt_obj = salt.client.LocalClient()


    def fetch_business_list(self):
        from config import business_list
        return business_list

    def gray_nginx_templete_set(self,host_ip_list,tag=True,business=None):
        if not business:
            business = self.business
        # print business
        nginx_file = "%s%s" % (nginx_config["root_dir"], nginx_config[business])
        for i in host_ip_list:
            if tag:
                ret = subprocess.Popen("sed -i '/%s/s/^/#/' %s" % (i,nginx_file),shell=True, cwd='/tmp/',stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print "配置nginx配置项，屏蔽部署服务器：",ret.stdout.read(),ret.stderr.read()
            else:
                ret = subprocess.Popen("sed -i '/%s/s/^#*//' %s" % (i, nginx_file), shell=True, cwd='/tmp/',stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print "配置nginx配置项，取消屏蔽：",ret.stdout.read(), ret.stderr.read()
            conf_ret = subprocess.Popen("grep %s %s" %(i,nginx_file),shell=True, cwd='/tmp/',stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print conf_ret.stdout.read(),conf_ret.stderr.read()
        return not ret.poll()

    def nginx_templete_push(self):
        # nginx_host_list = self.host_obj.fetch_nginx_host()
        # target_expr = self.host_obj.host_expr_generate(nginx_host_list)
        push_ret = self.salt_obj.cmd("G@business:nginx", "state.sls", [nginx_config["nginx_conf_push_sls"]], expr_form='compound')
        return push_ret

    def ret_check(self, deploy_ret):
        tag = True
        for i in deploy_ret.values():
            for x in i.values():
                if x["result"] == False:
                    tag = False
                    print x
        if tag:
            print "\033[31;1mOperation success..!!!\033[0m"
        else:
            sys.exit("\033[31;1mOperation faild..!!!\033[0m")
        return tag


    ##部署之前的相关配置
    def webserver_http_gray_before_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def weibao_http_gray_before_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def alipay_http_gray_before_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def baidu_http_gray_before_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def webserver_coreapi_gray_before_set(self, host_ip_list):
        self.gray_nginx_templete_set(host_ip_list,True,"webserver_http")
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def weibao_coreapi_gray_before_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def alipay_coreapi_gray_before_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def baidu_coreapi_gray_before_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def guanli_gray_before_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret



    ##部署之后的相关配置
    def webserver_http_gray_after_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def weibao_http_gray_after_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def alipay_http_gray_after_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def baidu_http_gray_after_set(self,host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret


    def webserver_coreapi_gray_after_set(self, host_ip_list):
        self.gray_nginx_templete_set(host_ip_list, False, "webserver_http")
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret


    def weibao_coreapi_gray_after_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret


    def alipay_coreapi_gray_after_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret


    def baidu_coreapi_gray_after_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

    def guanli_gray_after_set(self, host_ip_list):
        ret = self.gray_nginx_templete_set(host_ip_list,False)
        if ret:
            push_result=self.nginx_templete_push()
            print "推送nginx配置至nginx服务器："
            self.ret_check(push_result)
        return ret

