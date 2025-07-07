*** Settings ***
Library    cam_one.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***
${ip}    http://172.16.15.108
${id}    admin
${pass}    pass0001!

*** Test Cases ***
로그인
    Loginop    ${ip}    ${id}    ${pass}
녹화 시작_비디오스트림3
    Recon 3
    Op Stream
    Cama 11
    Op Stream Pb
    Cama 12
    Op Stream Pb
    Cama 13
    Op Stream Pb
녹화 시작_비디오스트림4
    Recon 4
    Op Stream
    Cama 14
    Op Stream Pb
    Cama 15
    Op Stream Pb
    Cama 16
    Op Stream Pb
    Cama 17