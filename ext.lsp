;;Garett Morrison
;;Weird patchwork code, but I'm learning lisp!
(defun printPoint (p1)
	(princ "\nx: ")
	(princ (car p1))
	(princ " y: ")
	(princ (cadr p1))
)

(defun printList (listIn)
	(setq listLen (length listIn)
		i 0
	)

	(princ "\nPrint List Len: ")
	(princ listLen)
	(while (< i listLen)
		(princ "\nIndex: ")
		(princ i)
		(princ " is ")
		(princ (nth i listIn))

		(setq i (1+ i))
	)
)

(defun getDist (p1 p2) 
	(setq xDiff (- (car  p2) (car  p1)))
	(setq yDiff (- (cadr p2) (cadr p1)))
	(sqrt (+ (expt xDiff 2) (expt yDiff 2)))
)

(defun extend (p1 p2 L) 
	(setq xDiff (- (car  p2) (car  p1))
	 yDiff (- (cadr p2) (cadr p1))
	 xDir  (if (> xDiff 0) 1 -1)
	 yDir  (if (> yDiff 0) 1 -1)
	 inLen (getDist p1 p2)
	)

	(if (= xDiff 0)
		(setq xOut (car p1) ;If vertical line, prevent div by 0 error
			yOut (+ (cadr p1) (* yDir L))
		) 
		(setq ratio (/ yDiff xDiff) ;basic trig to extend LINE
			xOut (+ (car   p1) (* L (/ xDiff inLen)))	;(+ (car  p1) (/ (* L xDiff      ) (sqrt (+ (expt ratio 2) 1))))
			yOut (+ (cadr  p1) (* L (/ yDiff inLen)))	;(+ (cadr p1) (/ (* L yDiff ratio) (sqrt (+ (expt ratio 2) 1))))
		)
	)

	(list xOut yOut 0.0)
)


(defun C:gext (/ ss n segs startPoint line)
	(setq ss (ssget '((0 . "LINE")))
		n (1- (sslength ss))
	)
	(setq len (getreal "\nEnter output length: "))
	; (princ "\nThis may take a minute.")
	(while (>= n 0)
		;get line entity
		(setq line (entget (ssname ss n)))

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


(defun C:gminext (/ ss n segs startPoint line)
	(setq ss (ssget '((0 . "LINE")))
		n (1- (sslength ss))
	)
	(setq len (getreal "\nEnter output length: "))
	; (princ "\nThis may take a minute.")
	(while (>= n 0)
		;get line entity
		(setq line (entget (ssname ss n)))

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

		; (princ len)
		; (princ " > ")
		; (princ (getDist p1 p2))
		
		;;;Save changes to line if is larger
		(cond 
			( ( > len (getDist p1 p2) ) ;If new line is longer
				(setq line (subst (cons (car (assoc 10 line)) pEx1) (assoc 10 line) line))
				(setq line (subst (cons (car (assoc 11 line)) pEx2) (assoc 11 line) line))
				
			)
		)

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