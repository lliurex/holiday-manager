import QtCore
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import org.kde.kirigami as Kirigami

Rectangle{
    id:rectLayout
    color:"transparent"
    Text{ 
        text:i18nd("holiday-manager","Configured holiday")
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
            visible:holidayStackBridge.showMainMessage.show
            text:getTextMessage(holidayStackBridge.showMainMessage.msgCode)
            type:getTypeMessage(
            holidayStackBridge.showMainMessage.type)
            Layout.minimumWidth:650
            Layout.fillWidth:true
            Layout.topMargin: 40
        }

        GridLayout{
            id: optionsGrid
            rows: 1
            flow: GridLayout.TopToBottom
            rowSpacing:10
            Layout.topMargin: messageLabel.visible?0:80
            
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
                    text:i18nd("holiday-manager","Generate backup")
                    enabled:holidayStackBridge.enableGlobalOptions
                    onClicked:{
                        backupAction="export"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to save holidays list")
                        backupFileDialog.fileMode=FileDialog.SaveFile
                        backupFileDialog.open()
                    }
                }

                MenuItem{
                    icon.name:"document-import.svg"
                    text:i18nd("holiday-manager","Import backup")
                    onClicked:{
                        backupAction="import"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to load holidays list")
			backupFileDialog.fileMode=FileDialog.OpenFile
                        importDatesDialog.open()

                    }
                }
           
            }
           
        }

       Button {
            id:deleteBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"delete.svg"
            text:i18nd("holiday-manager","Delete holidays list")
            Layout.preferredHeight:40
            enabled:holidayStackBridge.enableGlobalOptions
            Layout.rightMargin:rectLayout.width-(backupBtn.width+deleteBtn.width+newBtn.width+30)
            onClicked:holidayStackBridge.removeDate({"removeAll":true,"dateToRemove":""})
        }            
        Button {
            id:newBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add.svg"
            text:i18nd("holiday-manager","New holiday")
            Layout.preferredHeight:40
            onClicked:{
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

    ChangesDialog{
        id:removeDateDialog
        dialogIcon:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
        dialogMsg:{
            if (holidayStackBridge.showRemoveDateDialog.removeAll){
                i18nd("holiday-manager","The list of holidays will be deleted.\nDo yo want to continue?")
            }else{
                i18nd("holiday-manager","The holiday will be deleted.\nDo yo want to continue?")
            }
        }
        dialogVisible:holidayStackBridge.showRemoveDateDialog.show
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
        dialogMsg:i18nd("holiday-manager","New holidays list will be loaded and replace the existing configutation.\nDo you want to continue?")
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
                importDatesDialog.close()
           }

        }

    }

    FileDialog{
        id:backupFileDialog
        currentFolder:StandardPaths.standardLocations(StandardPaths.HomeLocation)[0]
        onAccepted:{
            var selectedPath=""
            selectedPath=backupFileDialog.selectedFile.toString()
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
    
    function getTextMessage(msgCode){
        switch (msgCode){
            case -1:
                return i18nd("holiday-manager","Unabled to apply changes. List blocked for other user")
            case -3:
                return i18nd("holiday-manager","Error saving changes")
            case -5:
                return i18nd("holiday-manager","Unabled to load holidays list")
            case -7:
                return i18nd("holiday-manager","Unabled to import list. List blocked for other user")
            case -8:
                return i18nd("holiday-manager","Error importing the list of holidays")
            case -9:
                return i18nd("holiday-manager","The list of holidays to be imported does not exist")
            case -11:
                return i18nd("holiday-manager","Error exporting the list of holidays")
            case 2:
                return i18nd("holiday-manager","Changes apply succesfully")
            case 3:
                return i18nd("holiday-manager","The list of holidays alreday removed. Nothing to do")
            case 5:
                return i18nd("holiday-manager","Holiday added successfully")
            case 6:
                return i18nd("holiday-manager","List of holidays imported successfully")
            case 7:
                return i18nd("holiday-manager","Holiday edited successfully")
            case 10:
                return i18nd("holiday-manager","List of holidays exported successfully")
            case 11:
                return i18nd("holiday-manager","Holiday deleted successfully")
            case 12:
                return i18nd("holiday-manager","The list of holidays deleted successfully")
            default:
                return ""
        }
        return msg
    } 

    function getTypeMessage(msgType){

        switch(msgType){
            case 0:
                return Kirigami.MessageType.Positive
            case 1:
                return Kirigami.MessageType.Error
            case 2:
                return Kirigami.MessageType.Warning
            case 3:
            default:
                return Kirigami.MessageType.Information
        }
    }


} 
