*** Settings ***
Library    cam_two.py
Library    SeleniumLibrary
Suite Setup    init_driver
*** Variables ***

*** Test Cases ***
로그인 테스트
    Login Option Image   http://172.16.15.108    admin   pass0001!
비디오&이미지 - 비디오 입력 - PAL
    Video Source PAL
    Reset Fix    admin    pass0001!
비디오&이미지 - 비디오 입력 - NTSC
    login short image   admin    pass0001!
    Video Source NTSC
    Reset Fix    admin    pass0001!
    login short image    admin    pass0001!
비디오&이미지 - 이미지 - 기본 탭
    Bright
    Saturation
    Contrast
    Tone
    Sharpness
    Reversal
    Logout
    Logout After Login Image    admin    pass0001!
비디오&이미지 - 이미지 - OSD 탭
    Osd
    Logout
    Logout After Login Image    admin    pass0001!
비디오&이미지 - 이미지 - 색온도 탭
    Faker
비디오&이미지 - 이미지 - 주 & 야간 탭
    Day Night
비디오&이미지 - 이미지 - 광역역광보정 탭
    Wdr
비디오&이미지 - 이미지 - 역광보정 탭
    Blc
비디오&이미지 - 이미지 - 노이즈 탭
    Noise
비디오&이미지 - 이미지 - 렌즈왜곡보정 탭
    Compensation
비디오&이미지 - 이미지 - 세로모드 탭
    Vertical
비디오&이미지 - 디지털 줌
    Digital Zoom
    Logout
    Logout After Login    admin    pass0001!