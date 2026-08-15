(defun c:AD_HOC_FOREACH ()
  (vl-load-com)  ; Load the Visual LISP extension
  (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))  ; Get the active AutoCAD document
  
  (setq layouts (vla-get-Layouts doc))  ; Get the Layouts collection
  
  (vlax-for layout layouts
    (if (/= (vla-get-Name layout) "Model")  ; Skip the Model layout
      (progn
        (vla-put-ActiveLayout doc layout)  ; Set the layout as active
        (command "AD_HOC")  ; Run the AD_HOC command
      )
    )
  )
  
  (alert "The recorded operation has been applied to all paper-space layouts.")  ; Display a message
)
