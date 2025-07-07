*** Settings ***
Library    cam_two.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***
${id}    admin
${pass}    pass0001!
${ip}    http://172.16.15.108

*** Test Cases ***
시스템 설정 - 보안
    Login Security    ${ip}    ${id}   ${pass} 
시스템 설정 - 관리 - 유저 추가 및 삭제
    User Add
    User Delete
시스템 설정 - 시간
    Logout
    Login Time    ${id}   ${pass} 
시스템 설정 - 시간 - 컴퓨터 시간과 동기화
    Local Time
시스템 설정 - 시간 - NTP 서버와 동기화
    ${result}=    Run Keyword And Ignore Error    Login Time    ${id}   ${pass}
    NTP Time
시스템 설정 - 시간 - 로그인 시간과 동기화
    ${result}=    Run Keyword And Ignore Error    Login Time    ${id}   ${pass}
    Login Same Time
시스템 설정 - 시간 - 써머타임
    ${result}=    Run Keyword And Ignore Error    Login Time    ${id}   ${pass}
    Summer Time
시스템 설정 - 시간 - 년-월-일 포맷
    Ymd 12
    Ymd 24
    Mdy 24
    Dmy 24

