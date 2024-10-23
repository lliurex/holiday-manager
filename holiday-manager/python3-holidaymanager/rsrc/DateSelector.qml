import org.kde.kirigami as Kirigami
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {

    id:dateSelectorPopUp
    width:530
    height:580
    anchors.centerIn: Overlay.overlay
    modal:true
    focus:true
    visible:holidayStackBridge.showDateForm
    closePolicy:Popup.NoAutoClose
    onVisibleChanged:{
        if (visible){
            loadInitValues()
        }
    }
    background:Rectangle{
        color:"#ebeced"
        border.color:"#b8b9ba"
        border.width:1
        radius:5.0

    }

    contentItem:Rectangle{
        id:container
        width:dateSelectorPopUp.width
        height:dateSelectorPopUp.height
        color:"transparent"
        Text{ 
            text:i18nd("holiday-manager","Edit holiday")
            font.pointSize: 16
        }
        GridLayout{
            id:dateSelectorLayout
            rows:3
            flow: GridLayout.TopToBottom
            rowSpacing:15
            anchors.left:parent.left
            anchors.bottomMargin:20
            anchors.horizontalCenter:parent.horizontalCenter
            enabled:true
           
            Kirigami.InlineMessage {
                id: messageLabel
                visible:false
                text:""
                type: Kirigami.MessageType.Error
                Layout.preferredWidth:505
                Layout.topMargin: 40
            }

            CustomCalendar{
                id:calendar
                Layout.alignment:Qt.AlignHCenter
                Layout.preferredWidth:325
                Layout.topMargin: messageLabel.visible?0:50
                currentLocale:Qt.locale(holidayStackBridge.systemLocale)
                startDate:undefined
                stopDate:undefined
                initDate:{
                    if (rangeDate.checked){
                        day1Entry.text
                    }else{
                        dayEntry.text
                    }
                }
                endDate:{
                    if (rangeDate.checked){
                        day2Entry.text
                    }else{
                        ""
                    }
                }
                rangeDate:rangeDate.checked
                daysInRange:holidayStackBridge.daysInRange
                currentMonth:new Date().getMonth()
                currentYear:new Date().getFullYear()
                fullMonth:new Date().toLocaleString(Qt.locale(),'MMMM').split(" ").slice(-1)[0]
                Connections{
                    target:calendar
                    function onGetSelectedDate(info){
                        if (rangeDate.checked){
                            if (info[1]=="start"){
                                day1Entry.text=info[0]
                                day2Entry.text=""
                            }else{
                                day2Entry.text=info[0]
                            }
                            dayEntry.text=""
                        }else{
                            dayEntry.text=info[0]
                            day1Entry.text=""
                            day2Entry.text=""
                            calendar.startDate=undefined
                        }
                    }
                }
            }
            
            GridLayout{
                id: dateOptions
                rows:3
                flow: GridLayout.TopToBottom
                rowSpacing:5
                Layout.fillWidth:true
                ButtonGroup{
                    id:dateOptionsGroup
                }
                
                RowLayout{
                    id:singleRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:singleDate
                        checked:!holidayStackBridge.dateRangeOption
                        text:i18nd("holiday-manager","Day:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:dayEntry 
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:singleDate.checked?true:false
                        
                    }

                }
                RowLayout{
                    id:rangeRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10
                    RadioButton{
                        id:rangeDate
                        checked:holidayStackBridge.dateRangeOption
                        text:i18nd("holiday-manager","From:")
                        ButtonGroup.group:dateOptionsGroup
                            
                    }
                    TextField{
                        id:day1Entry 
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:rangeDate.checked?true:false
                        
                    }
                    Text{
                        id:day2Text
                        text:i18nd("holiday-manager","to:")
                    }
                    TextField{
                        id:day2Entry 
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHCenter
                        readOnly:true
                        Layout.preferredWidth:100
                        enabled:rangeDate.checked?true:false
                    
                    }
        
                }
                RowLayout{
                    id:descriptionRow
                    spacing:10
                    Layout.alignment:Qt.AlignLeft
                    Layout.bottomMargin:10

                    Text{
                        id:descriptionText
                        text:i18nd("holiday-manager","Description:")
                    }
                    TextField{
                        id:descriptionEntry 
                        font.pointSize: 10
                        horizontalAlignment:TextInput.AlignHLeft
                        Layout.preferredWidth:250
                    }
                }
            }

        }
        RowLayout{
            id:btnBox
            anchors.bottom:parent.bottom
            anchors.right:parent.right
            anchors.topMargin:10
            spacing:10

            Button {
                id:applyBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-ok.svg"
                text:i18nd("holiday-manager","Apply")
                Layout.preferredHeight:40
                enabled:true
                onClicked:{
                    if (validateDates()){
                        var tmpValue=""
                        if (rangeDate.checked){
                            tmpValue=day1Entry.text+"-"+day2Entry.text
                        }else{
                            tmpValue=dayEntry.text
                        }
                        holidayStackBridge.applyDateChanges([tmpValue,descriptionEntry.text])
                    }
                }
            }
            
            Button {
                id:cancelBtn
                visible:true
                display:AbstractButton.TextBesideIcon
                icon.name:"dialog-cancel.svg"
                text:i18nd("holiday-manager","Cancel")
                Layout.preferredHeight: 40
                enabled:true
                onClicked:{
                    holidayStackBridge.closeDateForm()

                }
                
            }

        }
    }
    function validateDates(){

        if (rangeDate.checked){
            if ((day1Entry.text=="")&&(day2Entry.text="")){
                messageLabel.visible=true
                messageLabel.text=i18nd("holiday-manager","You must indicate the two dates of range")
                return false         
            }else{
                if (day2Entry.text==""){
                    messageLabel.visible=true
                    messageLabel.text=i18nd("holiday-manager","You must indicate the two dates of range")
                    return false
                }else{
                    if (Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")>=Date.fromLocaleString(Qt.locale(),day2Entry.text,"dd/MM/yyyy")){
                        messageLabel.visible=true
                        messageLabel.text=i18nd("holiday-manager","Last date in range must be major than init date")
                        return false
                    }else{
                        messageLabel.visible=false
                        messageLabel.text=""
                        return true
                    }
                }
            }
        }else{
            if (dayEntry.text==""){
                messageLabel.visible=true
                messageLabel.text=i18nd("holiday-manager","You must indicate the date")
                return false
            }else{
                messageLabel.visible=false
                messageLabel.text=""
                return true
            }
        }
    }

    function loadInitValues(){

        messageLabel.visible=false
        calendar.startDate=undefined
        calendar.stopDate=undefined
        calendar.daysInRange=holidayStackBridge.daysInRange
        rangeDate.checked=holidayStackBridge.dateRangeOption
	var newDate=new Date()

        
        if (holidayStackBridge.dateRangeOption){
            dayEntry.text=""
            if (holidayStackBridge.daysInRange.length>0){
                day1Entry.text=holidayStackBridge.daysInRange[0]
                day2Entry.text=holidayStackBridge.daysInRange[ holidayStackBridge.daysInRange.length-1]
                newDate=Date.fromLocaleString(Qt.locale(),day1Entry.text,"dd/MM/yyyy")
            }else{
                day1Entry.text=""
                day2Entry.text=""
                newDate=new Date()
            }
            calendar.initDate=day1Entry.text
            calendar.endDate=day2Entry.text
        }else{
            day1Entry.text=""
            day2Entry.text=""
            dayEntry.text=holidayStackBridge.daysInRange[0]
            calendar.initDate=dayEntry.text
            calendar.endDate=""
            if (dayEntry!=""){
                newDate=Date.fromLocaleString(Qt.locale(),dayEntry.text,"dd/MM/yyyy")
            }else{
                newDate=new Date()
            }

        }
        descriptionEntry.text=holidayStackBridge.dateDescription
	calendar.currentMonth=newDate.getMonth()
	calendar.currentYear=newDate.getFullYear()
	calendar.fullMonth=newDate.toLocaleString(Qt.locale(),'MMMM').split(" ").slice(-1)[0] 
 
    }

}
