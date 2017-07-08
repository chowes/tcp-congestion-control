import sys
import os

from subprocess import call


def __set_tcp_congestion_ctl(congestion_ctl='cubic'):
    if congestion_ctl == 'cubic':
        call(["sysctl", "-w", "net.ipv4.tcp_congestion_control=cubic"])
    elif congestion_ctl == 'reno':
        call(["sysctl", "-w", "net.ipv4.tcp_congestion_control=reno"])


def __enable_ecn():
    call(["sysctl", "-w", "net.ipv4.tcp_ecn=1"])


def __disable_ecn():
    call(["sysctl", "-w", "net.ipv4.tcp_ecn=0"])


def __enable_dctcp():
    call(["sysctl", "-w", "net.ipv4.tcp_dctcp_enable=1"])


def __disable_dctcp():
    call(["sysctl", "-w", "net.ipv4.tcp_dctcp_enable=0"])


def enable_dctcp():
    __set_tcp_congestion_ctl('reno')
    __enable_ecn()
    __enable_dctcp()


def disable_dctcp():
    __set_tcp_congestion_ctl('cubic')
    __disable_ecn()
    __disable_dctcp()
