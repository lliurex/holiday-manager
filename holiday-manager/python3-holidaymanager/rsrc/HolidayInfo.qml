import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.3
import org.kde.kirigami 2.16 as Kirigami

Rectangle{
    id:rectLayout
    color:"transparent"

    ColumnLayout{
        id:generalHolidaysLayout
        anchors.top:parent.top
        anchors.left:parent.left
        anchors.right:parent.right
        anchors.bottom:btnBox.top

        anchors.leftMargin:5
        anchors.rightMargin:15
        anchors.bottomMargin:25
        spacing: 10

        property var backupAction:undefined

        Text{ 
            text:i18nd("holiday-manager","Configured holiday")
            font.pointSize: 16
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:holidayStackBridge.showMainMessage.show
            text:getTextMessage(holidayStackBridge.showMainMessage.msgCode)
            type:getTypeMessage(
            holidayStackBridge.showMainMessage.type)
            Layout.fillWidth:true
        }

        HolidayList{
            id:holidayList
            holidayModel:holidayStackBridge.holidayModel
            Layout.fillHeight:true
            Layout.fillWidth:true
        }
    }

    RowLayout{
        id:btnBox
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin:5
        anchors.topMargin:20
        anchors.margins:15
        spacing: 30

        Button {
            id:backupBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"backup"
            text:i18nd("holiday-manager","Backup")
            onClicked:backupMenu.open()
            
            Menu{
                id:backupMenu
                y: -height - 5
                x: backupBtn.width/2

                MenuItem{
                    icon.name:"document-export"
                    text:i18nd("holiday-manager","Generate backup")
                    enabled:holidayStackBridge.enableGlobalOptions
                    onClicked:{
                        generalHolidaysLayout.backupAction="export"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to save holidays list")
                        backupFileDialog.selectExisting=false
                        backupFileDialog.open()
                    }
                }

                MenuItem{
                    icon.name:"document-import"
                    text:i18nd("holiday-manager","Import backup")
                    onClicked:{
                        generalHolidaysLayout.backupAction="import"
                        backupFileDialog.title=i18nd("holiday-manager","Please choose a file to load holidays list")
                        backupFileDialog.selectExisting=true
                        importDatesDialog.open()

                    }
                }
           
            }
           
        }

        Button {
             id:deleteBtn
             visible:true
             display:AbstractButton.TextBesideIcon
             icon.name:"delete"
             text:i18nd("holiday-manager","Delete holidays list")
             enabled:holidayStackBridge.enableGlobalOptions
             onClicked:holidayStackBridge.removeDate({"removeAll":true,"dateToRemove":""})
        } 

        Item{
            Layout.fillWidth:true
        }
           
        
        Button {
            id:newBtn
            visible:true
            display:AbstractButton.TextBesideIcon
            icon.name:"list-add"
            text:i18nd("holiday-manager","New holiday")
            onClicked:holidayStackBridge.addNewDate()
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
        dialogIcon:"dialog-warning"
        dialogTitle: holidayStackBridge.appName+" - "+i18nd("holiday-manager","Holiday List")
        dialogMsg:holidayStackBridge.showRemoveDateDialog.removeAll
                ?i18nd("holiday-manager","The list of holidays will be deleted.\nDo yo want to continue?")
                :i18nd("holiday-manager","The holiday will be deleted.\nDo yo want to continue?")
        
        dialogVisible:holidayStackBridge.showRemoveDateDialog.show
        dialogWidth:320
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardText:i18nd("holiday-manager","Accept")
        btnDiscardIcon:"dialog-ok"
        btnDiscardVisible:true
        btnCancelText:i18nd("holiday-manager","Cancel")
        btnCancelIcon:"dialog-cancel"
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
        dialogIcon:"dialog-warning"
        dialogTitle: holidayStackBridge.appName+" - "+i18nd("holiday-manager","Holiday List")
        dialogMsg:i18nd("holiday-manager","New holidays list will be loaded and replace the existing configutation.\nDo you want to continue?")
        dialogWidth:600
        btnAcceptVisible:false
        btnAcceptText:""
        btnDiscardVisible:true
        btnDiscardText:i18nd("holiday-manager","Accept")
        btnDiscardIcon:"dialog-ok"
        btnCancelText:i18nd("holiday-manager","Cancel")
        btnCancelIcon:"dialog-cancel"
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
        folder:shortcuts.home
        onAccepted:{
            var selectedPath=""
            selectedPath=backupFileDialog.fileUrl.toString()
            selectedPath=selectedPath.replace(/^(file:\/{2})/,"")
            switch(generalHolidaysLayout.backupAction){
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
