#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import salt.client


class Host(object):
    def __init__(self,business):
        self.salt_obj = salt.client.LocalClient()
        self.business_all_host = self.fetch_business_host(business)
        # print self.business_all_host

    def fetch_business_host(self,business):
        business_all_host = self.salt_obj.cmd("G@business:%s" % business,"grains.item",["business_ip"],expr_form='compound')
        return business_all_host

    def online(self,deploy_type,business):

        return "online"

    def gray(self,deploy_type,business):
        self.gray_host_set()
        return "gray"

    def gray_host_set(self):
        if len(self.business_all_host) < 4:
            gray_host_li = [self.business_all_host.keys()[0]]
        else:
            gray_host_li = [self.business_all_host.keys()[0],self.business_all_host.keys()[1]]
        print gray_host_li
        target_expr = ""
        for i in gray_host_li:
            if target_expr:
                target_expr = "L@s%" % i
            else:
                target_expr = "%s,%i" %(target_expr,i)
        print target_expr


    def gray_host_check(self):
        pass