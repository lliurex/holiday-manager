import org.kde.plasma.components as PC
import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQml.Models
import QtQuick.Layouts


Rectangle {
    property alias holidayModel:listDates.model
    
    id:datesTable
    visible: true
    Layout.fillHeight:true
    Layout.fillWidth:true
    color:"white"
    border.color: "#d3d3d3"

    PC.ScrollView{
        implicitWidth:parent.width
        implicitHeight:parent.height
        anchors.leftMargin:10

        ListView{
            id: listDates
            anchors.fill:parent
            height: parent.height
            enabled:true
            currentIndex:-1
            clip: true
            focus:true
            boundsBehavior: Flickable.StopAtBounds
            highlight: Rectangle { color: "#add8e6"; opacity:0.8;border.color:"#53a1c9" }
            highlightMoveDuration: 0
            highlightResizeDuration: 0
            model:holidayModel
            delegate: ListDelegateDateItem{
                width:datesTable.width
                dateId:model.id
                dateType:model.type
                dateDescription:model.description
            }
            Kirigami.PlaceholderMessage { 
                id: emptyHint
                anchors.centerIn: parent
                width: parent.width - (Kirigami.Units.largeSpacing * 4)
                visible: listDates.count==0?true:false
                text: i18nd("holiday-manager","No holiday is configured")
            } 
         }
    }
}

