*** Settings ***
Library       C:/Users/marcospaulo_frwk/PycharmProjects/robotframework-testnotify/TestNotification    https://chat.googleapis.com/v1/spaces/AAAAx2DKvtk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_H3a5vSbt83PopSfxDDAidvf_6Ft-r5qlV-g8izJ3Vg    google    end_suite


*** Test Cases ***
VAlidar

    Log To Console     TEstes

VAlidar 2

    Fail   teste