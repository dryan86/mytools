#!/bin/bash

iptables -F

iptables -X

#shell执行

iptables -P INPUT DROP

iptables -P OUTPUT DROP

iptables -P FORWARD DROP

#开启SSH 22端口

iptables -A INPUT -p tcp --dport 22 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

#ngnix服务器默认端口，网站可访问

iptables -A INPUT -p tcp --dport 80 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT

#允许ping

iptables -A INPUT -p icmp -j ACCEPT

iptables -A OUTPUT -p icmp -j ACCEPT

#允许loopback，不然会导致DNS无法正常关闭等问题

iptables -A INPUT -i lo -p all -j ACCEPT

iptables -A OUTPUT -o lo -p all -j ACCEPT

#丢弃坏的TCP包

iptables -A FORWARD -p TCP ! --syn -m state --state NEW -j DROP

#处理IP碎片数量,防止攻击,允许每秒100个

iptables -A FORWARD -f -m limit --limit 100/s --limit-burst 100 -j ACCEPT

#设置ICMP包过滤,允许每秒1个包,限制触发条件是10个包

iptables -A FORWARD -p icmp -m limit --limit 1/s --limit-burst 10 -j ACCEPT

#开启对指定网站的访问

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A OUTPUT -m state --state NEW,ESTABLISHED,RELATED -p tcp -d www.github.com -j ACCEPT

#重启使生效

/etc/rc.d/init.d/iptables save

service iptables restart