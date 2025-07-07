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
녹화 옵션 설정
    Recon
    Reckeep
    Rectimer
녹화 시작_비디오스트림 1
    Op Stream
    Cama 1
    Op Stream Pb
    Cama 2
    Op Stream Pb
    Cama 3
    Op Stream Pb
    Cama 4
녹화 시작_비디오스트림2
    Recon 2
    Op Stream
    Cama 5
    Op Stream Pb
    Cama 6
    Op Stream Pb
    Cama 7
    Op Stream Pb
    Cama 8
    Op Stream Pb
    Cama 9
    Op Stream Pb