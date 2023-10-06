(define-sort A () (Array Int Int))

(declare-fun b () Int)
(declare-fun c () Int)
(declare-fun f (Int) Int)
(declare-fun a () A)

(assert (= b (+ c 3)))
(assert (= (f b) (- c 1)))
(assert (= 
    (select a (f (+ c 3)))
    (+ b 1)
))
(assert (or
    (= (select a (f b)) c)
    (= 
        (select (store a b (f (+ c 3))) (f b))
        (+ c 4)
    )
))

(check-sat)
(get-model)
