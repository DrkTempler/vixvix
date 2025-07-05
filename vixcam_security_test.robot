*** Settings ***
Library    cam_two.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***

*** Test Cases ***
시스템 설정 - 보안
    Login Security    http://172.16.15.108    admin    pass0001!
시스템 설정 - 관리 - 유저 추가 및 삭제
    User Add
    User Delete
시스템 설정 - 시간
    Login Time    admin    pass0001!