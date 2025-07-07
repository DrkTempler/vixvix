*** Settings ***
Library    cam_two.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***

*** Test Cases ***
로그인
    login   http://172.16.15.108    admin   pass0001!
라이브 스트림
    Livestream
라이브 스트림 - 포커스 조정
    Focus
라이브 스트림 - 다이렉트 줌
    Directzoom
라이브 스트림 - 줌인 줌아웃
    Zoom
    Logout