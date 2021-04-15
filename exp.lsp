;;Garett Morrison
;;Breaks polylines into segs
(defun C:gexp (/ ss n segs startPoint)
	(setq ss (ssget '((0 . "LINE,POLYLINE,LWPOLYLINE,ARC,CIRCLE")))
		n (1- (sslength ss))
	)
	(while (>= n 0)
		(command "pedit" (ssname ss n) "Decurve" "" )
		(command "explode" (ssname ss n) "" )
		(setq n (1- n))
	)
	(princ)
)

(defun C:gseg (/ ss n segs startPoint)
	(setq ss (ssget '((0 . "LINE,POLYLINE,LWPOLYLINE,ARC,CIRCLE")))
		n (1- (sslength ss))
	)
	(while (>= n 0)
		(command "pedit" (ssname ss n) "Decurve" "" )
		; (command "explode" (ssname ss n) "" ) ;Skip explode, allows you to still move polyines in chunks
		(setq n (1- n))
	)
)