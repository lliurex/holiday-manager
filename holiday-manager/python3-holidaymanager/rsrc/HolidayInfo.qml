import org.kde.plasma.core 2.1 as PlasmaCore
import org.kde.kirigami 2.16 as Kirigami
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3

Rectangle{
    id:rectLayout
    color:"transparent"
    Text{ 
        text:i18nd("holiday-manager","Configured holiday")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    property var backupAction:undefined

    GridLayout{
        id:generalHolidaysLayout
        rows:2
        flow: GridLayout.TopToBottom
        rowSpacing:10
        anchors.left:parent.left
        width:parent.width-10
        height:parent.height-90
        enabled:true
        Kirigami.InlineMessage {
            id: messageLabel
            visible:holidayStackBridge.showMainMessage[0]
            text:getTextMessage(holidayStackBridge.showMainMessage[1])
            type:getTypeMessage(
            holidayStackBridge.showMainMessage[2])
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.topMargin: messageLabel.visible?0:40
            
            HolidayList{
                id:holidayList
                holidayModel:holidayStackBridge.holidayModel
                Layout.fillHeight:true
                Layout.fillWidth:true
            }
        }
    }
    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.fill:parent.fill
        anchors.bottomMargin:15
        spacing:10

        Button {
            id:backupBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"backup.svg"
            text:i18nd("holiday-manager","Backup")
            Layout.preferredHeight:40
            onClicked:backupMenu.open()
            
            Menu{
                id:backupMenu
                y: -backupBtn.height*1.7
                x: backupBtn.width/2

                MenuItem{
                    icon.name:"document-export.svg"
                    text:i18nd("holiday-manager","Generate holidays backup")
                    /*enabled:holidayStackBridge.enableGlobalOptions
                    onClicked:{
                        
                        backupAction="export"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to save day list")
                        backupFileDialog.selectExisting=false
                        backupFileDialog.open()
                    }
                    */
                }

                MenuItem{
                    icon.name:"document-import.svg"
                    text:i18nd("holiday-manager","Import holidays backup")
                    /*onClicked:{

                        backupAction="import"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to load holidays list")
                        backupFileDialog.selectExisting=true
                        importBellDialog.open()

                    }
                    */
                }
           
            }
           
        }

        Button {
            id:deleteBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"delete.svg"
            text:i18nd("holiday-manager","Delete holidays list")
            Layout.preferredHeight:40
            /*enabled:holidayStackBridge.enableGlobalOptions*/
            Layout.rightMargin:rectLayout.width-(backupBtn.width+deleteBtn.width+newBtn.width+30)
            /*onClicked:actionsMenu.open()*/
        }            
        Button {
            id:newBtn
            visible:true
            focus:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add.svg"
            text:i18nd("holiday-manager","New date")
            Layout.preferredHeight:40
            Keys.onReturnPressed: applyBtn.clicked()
            Keys.onEnterPressed: applyBtn.clicked()
            onClicked:{
                console.log("1")
                holidayStackBridge.addNewDate()
            }
        }
    }
    
    CustomPopUp{
        id:waitingForm
    }
    
    DateSelector{
        id:dateSelector
    }
    /*
    ChangesDialog{
        id:removeDateDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"holiday-manager"+" - "+i18nd("holiday-manager","Holiday List")
        dialogMsg:{
            if (holidayStackBridge.showRemoveDateDialog[1]){
                i18nd("holiday-manager","All dates will be deleted.\nDo yo want to continue?")
            }else{
                i18nd("holiday-manager","The date will be deleted.\nDo yo want to continue?")
            }
        }
        dialogVisible:holidayStackBridge.showRemoveDateDialog[0]
        dialogWidth:300
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("holiday-manager","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnDiscardVisible:true
        btnCancelText:i18nd("holiday-manager","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:removeDateDialog
           function onDiscardDialogClicked(){
                holidayStackBridge.manageRemoveDateDialog('Accept')         
           }
           function onRejectDialogClicked(){
                holidayStackBridge.manageRemoveDateDialog('Cancel')       
           }

        }
    }

    ChangesDialog{
        id:importDatesDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogTitle:"holiday-manager"+" - "+i18nd("holiday-manager","Holiday List")
        dialogMsg:i18nd("holiday-manager","New dates list will be loaded and replace the existing configutarion.\nDo you want to continue?")
        dialogWidth:600
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardVisible:true
        btnDiscardText:i18nd("holiday-manager","Accept")
        btnDiscardIcon:"dialog-ok.svg"
        btnCancelText:i18nd("holiday-manager","Cancel")
        btnCancelIcon:"dialog-cancel.svg"
        Connections{
           target:importDatesDialog
           function onDiscardDialogClicked(){
                importDatesDialog.close()
                backupFileDialog.open()
           }
           function onRejectDialogClicked(){
                importBellDialog.close()
           }

        }

    }

    FileDialog{
        id:backupFileDialog
        folder:shortcuts.home
        nameFilters:["Zip files (*zip)"]
        onAccepted:{
            var selectedPath=""
            selectedPath=backupFileDialog.fileUrl.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            switch(backupAction){
                case "export":
                    holidayStackBridge.exportDatesConfig(selectedPath)
                    break;
                case "import":
                    holidayStackBridge.importDatesConfig(selectedPath)
                    break;
            }

        }
      
    }
    */
    function getTextMessage(msgCode){
        switch (msgCode){
            case -1:
                var msg=i18nd("holiday-manager","Unabled to apply changes. List blocked for other user")
                break;
            case -3:
                var msg=i18nd("holiday-manager","Error saving changes")
                break;
            case -5:
                var msg=i18nd("holiday-manager","Unabled to load date list")
                breal;
            case -7:
                var msg=i18nd("holiday-manager","Unabled to import list. List blocked for other user")
                break;
            case -8:
                var msg=i18nd("holiday-manager","Error importing the list of dates")
                break;
            case -9:
                var msg=i18nd("holiday-manager","The list of dates to be imported does not exist")
                break;
            case -11:
                var msg=i18nd("holiday-manager","Error exporting the list of dates")
                break;
            case 2:
                var msg=i18nd("holiday-manager","Changes apply succesfully")
                break;
            case 6:
                var msg=i18nd("holiday-manager","List of dates imported successfully")
                break;
            case 10:
                var msg=i18nd("holiday-manager","List of dates exported successfully")
                break;
            default:
                var msg=""
                break;
        }
        return msg
    } 

    function getTypeMessage(msgType){

        switch (msgType){
            case "Information":
                return Kirigami.MessageType.Information
            case "Ok":
                return Kirigami.MessageType.Positive
            case "Error":
                return Kirigami.MessageType.Error
            case "Warning":
                return Kirigami.MessageType.Warning
        }
    }

} 
