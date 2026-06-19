import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: popUpWaiting
    width: 570
    height: 100
    anchors.centerIn: Overlay.overlay
    modal: true
    focus: true
    visible: holidayStackBridge.showPopUp.show
    closePolicy: Popup.NoAutoClose

    background: Rectangle {
        color: palette.window
        border.color: palette.mid
        radius: 4
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Image{
            id:spinnerImage
            source: "/usr/lib/python3/dist-packages/holidaymanager/rsrc/loading.png"
            Layout.preferredWidth: 24
            Layout.preferredHeight: 24
            Layout.alignment: Qt.AlignHCenter
            fillMode: Image.PreserveAspectFit
            smooth:false
            antialiasing:false

            rotation:0
        }
            
        Timer{
            id:rotationTimer
            running:(spinnerImage!==null && popUpWaiting!==null) && spinnerImage.visible && popUpWaiting.visible
            repeat:true
            interval:100

            onTriggered:{
                spinnerImage.rotation=(spinnerImage.rotation+330)%360
            }
        }

        Text {
            id: popupText
            text: getTextMessage()
            font.pointSize: 10
            color: palette.windowText
            Layout.alignment: Qt.AlignHCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    function getTextMessage(){
        switch (holidayStackBridge.showPopUp.msgCode){
            case 1:
                return i18nd("holiday-manager","Loading. Wait a moment...");
            case 2:
                return i18nd("holiday-manager","Applying changes. Wait a moment...")
            case 3:
                return i18nd("holiday-manager","Exporting holidays configuration. Wait a moment...")
            case 4:
                return i18nd("holiday-manager","Loading holidays configuration. Wait a moment...")
            default:
                return ""
        }
    }
}
