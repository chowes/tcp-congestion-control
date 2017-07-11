import sys
import os

from subprocess import Popen


def __set_tcp_congestion_ctl(congestion_ctl='cubic'):
    if congestion_ctl == 'cubic':
        Popen("sysctl -w net.ipv4.tcp_congestion_control=cubic",
              shell=True).wait()
    elif congestion_ctl == 'reno':
        Popen("sysctl -w net.ipv4.tcp_congestion_control=reno",
              shell=True).wait()


def __enable_ecn():
    Popen("sysctl -w net.ipv4.tcp_ecn=1",
          shell=True).wait()


def __disable_ecn():
    Popen("sysctl -w net.ipv4.tcp_ecn=0",
          shell=True).wait()


def __enable_dctcp():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=1",
          shell=True).wait()


def __disable_dctcp():
    Popen("sysctl -w net.ipv4.tcp_dctcp_enable=0",
          shell=True).wait()


def enable_dctcp():
    __set_tcp_congestion_ctl('reno')
    __enable_ecn()
    __enable_dctcp()


def disable_dctcp():
    __set_tcp_congestion_ctl('reno')
    __disable_ecn()
    __disable_dctcp()


def reset_tcp():
    __set_tcp_congestion_ctl('cubic')
    __disable_ecn()
    __disable_dctcp()
