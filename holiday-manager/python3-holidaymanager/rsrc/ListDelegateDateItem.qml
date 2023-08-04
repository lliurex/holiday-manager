import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQml.Models 2.8
import org.kde.plasma.components 2.0 as Components


Components.ListItem{

    id: listDateItem
    property string dateId
    property string dateType
    property string dateDescription

    enabled:true

    onContainsMouseChanged: {
        if (!optionsMenu.activeFocus){
            if (containsMouse) {
                listDates.currentIndex = index
            }else {
                listDates.currentIndex = -1
            }
        }

    }

    Item{
        id: menuItem
        height:visible?60:0
        width:parent.width-manageDateBtn.width

        Image{
            id:dateImage
            width:48
            height:48
            fillMode:Image.PreserveAspectFit
            source:{
                if (dateType=="single"){
                    "/usr/lib/python3/dist-packages/holidaymanager/rsrc/calendar_day.png"
                }else{
                    "/usr/lib/python3/dist-packages/holidaymanager/rsrc/calendar_range_day.png"
              }
            }
            anchors.verticalCenter:parent.verticalCenter
            anchors.leftMargin:20
        }
        Text{
            id:dateText
            text:dateId
            font.family: "Quattrocento Sans Bold"
            font.pointSize: 10
            horizontalAlignment:Text.AlignLeft
            width:80
            anchors.left:dateImage.right
            anchors.leftMargin:20
            anchors.verticalCenter:parent.verticalCenter

        }

        Text{
            id:descriptionText
            text:dateDescription
            font.family:"Quattrocento Sans Bold"
            font.pointSize: 10
            horizontalAlignment:Text.AlignLeft
            elide:Text.ElideMiddle
            width:{
                if (listDateItem.ListView.isCurretItem){
                    parent.width-(dateImage.width+dateText.width+manageDateBtn.width+150)
                }else{
                  parent.width-(dateImage.width+dateText.width+150)
                }
            }
            anchors.left:dateText.right
            anchors.leftMargin:dateText.width+20
            anchors.verticalCenter:parent.verticalCenter
        }

        Button{
            id:manageDateBtn
            display:AbstractButton.IconOnly
            icon.name:"configure.svg"
            anchors.leftMargin:15
            anchors.left:descriptionText.right
            anchors.verticalCenter:parent.verticalCenter
            visible:listDateItem.ListView.isCurrentItem
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("holiday-manager","Click to manage this date")
            onClicked:optionsMenu.open();
            onVisibleChanged:{
                optionsMenu.close()
            }

            Menu{
                id:optionsMenu
                y: manageDateBtn.height
                x:-(optionsMenu.width-manageDateBtn.width/2)

                MenuItem{
                    icon.name:"document-edit.svg"
                    text:i18nd("holiday-manager","Edit date")
                    onClicked:{
                        holidayStackBridge.loadDate(dateId)
                    }
                }
                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("holiday-manager","Delete the date")
                    /*onClicked:holidayStackBridge.removeDate(dateId)*/
                }
            }
        }
    }
}
