Attribute VB_Name = "Module1"
Sub ChangeOLEQualityToMonochrome()
    Dim doc As AcadDocument
    Dim layout As AcadLayout
    Dim Obj As Object
    

    Set doc = ThisDrawing

    ' Loop through all paper space layouts
    For Each layout In doc.Layouts
        doc.ActiveLayout = layout
        
        ' Loop through OLE objects in paper space
        For Each Obj In doc.PaperSpace
            If TypeOf Obj Is AcadOle Then
                Obj.OlePlotQuality = acOPQMonochrome
            End If
        Next Obj
    Next layout

    MsgBox "OLE object qualities on Layouts changed to monochrome."
End Sub
