(define-sort A () (Array Int Int))

(declare-fun b () Int)
(declare-fun c () Int)
(declare-fun f (Int) Int)
(declare-fun a () A)

(assert (= (- b 1) (+ c 3)))
(assert (not (= (f b) (+ b 1))))
(assert (= (select a (f (+ c 4))) (+ c 3)))

(assert
    (or
        (= (select a (f b)) (+ b 2))
        (= 
            (select
                (store a (+ b 1) (f (+ c 3)))
                (f (+ c 4))
            )
            (+ c 5)
        )
    )
)

(check-sat)

