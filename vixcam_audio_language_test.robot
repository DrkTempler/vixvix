*** Settings ***
Library    cam_two.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***
${id}    admin
${pass}    pass0001!
${ip}    http://172.16.15.108

*** Test Cases ***
오디오 로그인
    Login Audio    ${ip}    ${id}    ${pass}
오디오 UI 테스트
    Audio Activate
    Audio Option Check
    Logout
언어 로그인
    Login Language    ${ip}    ${id}    ${pass}
언어 변경
    Language English
    Language Korean
로그인 실패 테스트
    Login Fail Test    ${ip}    ${id}
