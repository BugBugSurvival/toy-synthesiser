
(set-logic LIA)

(synth-fun max3 ((x Int) (y Int) (z Int)) Int
((Start Int) (x Int) (y Int) (z Int) (StartBool Bool))
    ((Start Int (x
                 y
                 z
                 (ite StartBool Start Start)))
     (StartBool Bool ((or  StartBool StartBool)
                      (<=  Start Start)
                      (=   Start Start)))))

(declare-var x Int)
(declare-var y Int)
(declare-var z Int)

(constraint (>= (max3 x y z) x))
(constraint (>= (max3 x y z) y))
(constraint (>= (max3 x y z) z))
(constraint (or (= x (max3 x y z))
            (or (= y (max3 x y z))
                (= z (max3 x y z)))))

(check-synth)

