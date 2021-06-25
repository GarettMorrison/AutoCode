;;Garett Morrison
;;Weird patchwork code, but I'm learning lisp!

(defun C:delInternal (/ ss n segs startPoint line)
	(setq ss (ssget '((0 . "LINE")))
		n (1- (sslength ss))
	)
	; (princ "\nThis may take a minute.")
	(while (>= n 0)
		;get line entity
		(setq line (entget (ssname ss n)))
		(setq p1 (cdr (assoc 10 line)))
		(setq p2 (cdr (assoc 11 line)))

		(setq ptSum (0))
		(for checkIndex from 0 to n-1 (
			(setq lineCheck (entget (ssname ss checkIndex)))
			(setq cp1 (cdr (assoc 10 lineCheck)))
			(setq cp2 (cdr (assoc 11 lineCheck)))

			(if (equalp (p1, cp1) (setq ptSum (+ ptSum 1)))
			(if (equalp (p1, cp2) (setq ptSum (+ ptSum 1)))
			(if (equalp (p2, cp1) (setq ptSum (+ ptSum 1)))
			(if (equalp (p2, cp2) (setq ptSum (+ ptSum 1)))
		))

		(if (> ptSum 2) ())

		;get endpoints
		(setq p1 (cdr (assoc 10 line)))
		(setq p2 (cdr (assoc 11 line)))

		;Get midpoint
		(setq x (/ (- (car  p2) (car p1)) 2.00))
		(setq y (/ (- (cadr p2) (cadr p1)) 2.00))
		(setq midpoint (list (+ (car p1) x) (+ (cadr p1) y) 0.0))

		;Get new endpoint
		(setq pEx1 (extend midpoint p1 (/ len 2)))
		(setq pEx2 (extend midpoint p2 (/ len 2)))

		;Save changes to line
		(setq line (subst (cons (car (assoc 10 line)) pEx1) (assoc 10 line) line))
		(setq line (subst (cons (car (assoc 11 line)) pEx2) (assoc 11 line) line))
		(entmod line)
		
		;print info
		; (princ "\n")
		; (printPoint p1)
		; (printPoint p2)
		; (printPoint midpoint)
		; (printPoint pEx1)
		; (printPoint pEx2)
		; (princ "\nOrig Dist: ")
		; (princ (getDist p1 p2))
		; (princ "\nOutput Dist: ")
		; (princ (getDist pEx1 pEx2))

		;Iterate
		(setq n (1- n))
	)
	(princ "\n\nDONE!")
	(princ "\n")
	(princ)
)