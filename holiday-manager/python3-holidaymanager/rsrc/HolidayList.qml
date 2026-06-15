import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQml.Models
import QtQuick.Layouts


Rectangle {
    property alias holidayModel:listDates.model
    
    id:datesTable
    Layout.fillHeight:true
    Layout.fillWidth:true
    color:"white"
    border.color: "#d3d3d3"


    PC.ScrollView{
        anchors.fill:parent

        ListView{
            id: listDates
            model:holidayModel
            delegate: ListDelegateDateItem{
                width:datesTable.width-18
                dateId:model.id
                dateType:model.type
                dateDescription:model.description
            }

            currentIndex:-1
            enabled:true
            clip: true
            focus:true
            boundsBehavior: Flickable.StopAtBounds
            highlightFollowsCurrentItem:true
            highlightMoveDuration: 0
            highlightResizeDuration: 0

            Kirigami.PlaceholderMessage { 
                id: emptyHint
                anchors.centerIn: parent
                width: parent.width - (Kirigami.Units.largeSpacing * 4)
                visible: listDates.count==0?true:false
                text: i18nd("holiday-manager","No holiday is configured")
                icon.name:"/usr/lib/python3/dist-packages/holidaymanager/rsrc/calendar_range_day.png"
            } 
         }
    }
}

