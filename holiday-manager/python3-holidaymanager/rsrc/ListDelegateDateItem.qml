import QtQuick
import QtQuick.Controls
import QtQml.Models
import org.kde.plasma.components as Components


Components.ItemDelegate{

    id: listDateItem
    property string dateId
    property string dateType
    property string dateDescription

    height:65
    enabled:true

    Item{
        id: menuItem
        height:visible?60:0
        width:parent.width-manageDateBtn.width

        MouseArea {
            id: mouseAreaOption
            anchors.fill: parent
            hoverEnabled:true
            propagateComposedEvents:true

            onEntered: {
                listDates.currentIndex=index
            }
        }


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
	    anchors.left:parent.left
            anchors.verticalCenter:parent.verticalCenter
            anchors.leftMargin:10
        }
        Text{
            id:dateText
            text:dateId
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
            font.pointSize: 10
            horizontalAlignment:Text.AlignLeft
            elide:Text.ElideMiddle
            width:{
                if (listDateItem.ListView.isCurretItem){
                    parent.width-(dateImage.width+dateText.width+manageDateBtn.width+160)
                }else{
                  parent.width-(dateImage.width+dateText.width+160)
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
            ToolTip.text:i18nd("holiday-manager","Click to manage the holiday")
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
                    text:i18nd("holiday-manager","Edit holiday")
                    onClicked:{
                        holidayStackBridge.loadDate(dateId)
                    }
                }
                MenuItem{
                    icon.name:"delete.svg"
                    text:i18nd("holiday-manager","Delete the holiday")
                    onClicked:holidayStackBridge.removeDate([false,dateId])
                }
            }
        }
    }
}
