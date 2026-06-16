import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


ItemDelegate{

    id: listDateItem

    property string dateId
    property string dateType
    property string dateDescription

    height:70
    enabled:true

    width: listDateItem.ListView.view?listDateItem.ListView.view.width -10 : 0
    hoverEnabled:true

    leftPadding:10
    rightPadding:10

    onHoveredChanged:{
        if (hovered){
            if (listDateItem.ListView.view && !optionsMenu.opened){
                listDateItem.ListView.view.currentIndex=index
            }
        }else{
            if (!optionsMenu.opened && listDateItem.ListView.view){
                listDateItem.ListView.view.currentIndex=-1
            }
        }
    }

    background:Rectangle {
        x:5
        y:5
        width:parent.width-5
        height:parent.height-5
        color: (listDateItem.hovered || listDateItem.ListView.isCurrentItem || optionsMenu.opened)
               ?Qt.alpha(Kirigami.Theme.highlightColor,0.15)
               :"transparent"
        radius:6
        border.width:1
        border.color:(listDateItem.hovered || listDateItem.ListView.isCurrentItem || optionsMenu.opened)
                      ?Kirigami.Theme.highlightColor
                      :"transparent"
    }

    contentItem:RowLayout {
        spacing:20

        Image{
            id:dateImage
            Layout.preferredWidth:48
            Layout.preferredHeight:48
            fillMode:Image.PreserveAspectFit
            source:{
                if (dateType=="single"){
                    "/usr/lib/python3/dist-packages/holidaymanager/rsrc/calendar_day.png"
                }else{
                    "/usr/lib/python3/dist-packages/holidaymanager/rsrc/calendar_range_day.png"
              }
            }
	    }
        
        Text{
            id:dateText
            text:dateId
            font.pointSize: 10
            horizontalAlignment:Text.AlignLeft
            Layout.alignment: Qt.AlignVCenter
            width:80
        }

        Text{
            id:descriptionText
            text:dateDescription
            font.pointSize: 10
            horizontalAlignment:Text.AlignLeft
            elide:Text.ElideMiddle
            Layout.alignment: Qt.AlignVCenter
            Layout.fillWidth:true
        }

        Button{
            id:manageDateBtn
            display:AbstractButton.IconOnly
            icon.name:"configure"
            Layout.alignment: Qt.AlignVCenter
            visible:listDateItem.ListView.isCurrentItem || listDateItem.hovered || optionsMenu.opened
            ToolTip.delay: 1000
            ToolTip.timeout: 3000
            ToolTip.visible: hovered
            ToolTip.text:i18nd("holiday-manager","Click to manage the holiday")
            onClicked:optionsMenu.open();
            Connections{
                target:listDates
                function onCurrentIndexChanged(){
                    if (!listDateItem.ListView.isCurrentItem && optionsMenu.opened){
                        optionsMenu.close()
                    }

                }
            }

            Menu{
                id:optionsMenu
                y: manageDateBtn.height
                x:-(optionsMenu.width-manageDateBtn.width/2)

                MenuItem{
                    icon.name:"document-edit"
                    text:i18nd("holiday-manager","Edit holiday")
                    onClicked:{
                        holidayStackBridge.loadDate(dateId)
                    }
                }
                MenuItem{
                    icon.name:"delete"
                    text:i18nd("holiday-manager","Delete the holiday")
                    onClicked:holidayStackBridge.removeDate({"removeAll":false,"dateToRemove":dateId})
                }
            }
        }
    }
}
