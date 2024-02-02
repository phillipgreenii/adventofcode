(ns advent-of-code.core
  (:require [advent-of-code.support]
            [advent-of-code.day-01]
            [advent-of-code.day-02]
            [advent-of-code.day-03]
            [advent-of-code.day-04]
            [advent-of-code.day-05]
            [advent-of-code.day-06]
            [advent-of-code.day-07]
            [advent-of-code.day-08]
            [advent-of-code.day-09]
            [advent-of-code.day-10]
            [advent-of-code.day-11]
            [advent-of-code.day-12]
            [advent-of-code.day-13]
            [advent-of-code.day-14]
            [advent-of-code.day-15]
            [advent-of-code.day-16]
            [advent-of-code.day-17]
            [advent-of-code.day-18]
            [advent-of-code.day-19]
            [advent-of-code.day-20]
            [advent-of-code.day-21]
            [advent-of-code.day-22]
            [advent-of-code.day-23]
            [advent-of-code.day-24]
            [advent-of-code.day-25]))

(defn -main
  "Used to dispatch tasks from the command line.
  
  lein run d01.p1"
  [part]
  (case part
    "d01.p1" (println (advent-of-code.day-01/part-1 (advent-of-code.support/read-input  1 1)))
    "d01.p2" (println (advent-of-code.day-01/part-2 (advent-of-code.support/read-input  1 2)))
    "d02.p1" (println (advent-of-code.day-02/part-1 (advent-of-code.support/read-input  2 1)))
    "d02.p2" (println (advent-of-code.day-02/part-2 (advent-of-code.support/read-input  2 2)))
    "d03.p1" (println (advent-of-code.day-03/part-1 (advent-of-code.support/read-input  3 1)))
    "d03.p2" (println (advent-of-code.day-03/part-2 (advent-of-code.support/read-input  3 2)))
    "d04.p1" (println (advent-of-code.day-04/part-1 (advent-of-code.support/read-input  4 1)))
    "d04.p2" (println (advent-of-code.day-04/part-2 (advent-of-code.support/read-input  4 2)))
    "d05.p1" (println (advent-of-code.day-05/part-1 (advent-of-code.support/read-input  5 1)))
    "d05.p2" (println (advent-of-code.day-05/part-2 (advent-of-code.support/read-input  5 2)))
    "d06.p1" (println (advent-of-code.day-06/part-1 (advent-of-code.support/read-input  6 1)))
    "d06.p2" (println (advent-of-code.day-06/part-2 (advent-of-code.support/read-input  6 2)))
    "d07.p1" (println (advent-of-code.day-07/part-1 (advent-of-code.support/read-input  7 1)))
    "d07.p2" (println (advent-of-code.day-07/part-2 (advent-of-code.support/read-input  7 2)))
    "d08.p1" (println (advent-of-code.day-08/part-1 (advent-of-code.support/read-input  8 1)))
    "d08.p2" (println (advent-of-code.day-08/part-2 (advent-of-code.support/read-input  8 2)))
    "d09.p1" (println (advent-of-code.day-09/part-1 (advent-of-code.support/read-input  9 1)))
    "d09.p2" (println (advent-of-code.day-09/part-2 (advent-of-code.support/read-input  9 2)))
    "d10.p1" (println (advent-of-code.day-10/part-1 (advent-of-code.support/read-input 10 1)))
    "d10.p2" (println (advent-of-code.day-10/part-2 (advent-of-code.support/read-input 10 2)))
    "d11.p1" (println (advent-of-code.day-11/part-1 (advent-of-code.support/read-input 11 1)))
    "d11.p2" (println (advent-of-code.day-11/part-2 (advent-of-code.support/read-input 11 2)))
    "d12.p1" (println (advent-of-code.day-12/part-1 (advent-of-code.support/read-input 12 1)))
    "d12.p2" (println (advent-of-code.day-12/part-2 (advent-of-code.support/read-input 12 2)))
    "d13.p1" (println (advent-of-code.day-13/part-1 (advent-of-code.support/read-input 13 1)))
    "d13.p2" (println (advent-of-code.day-13/part-2 (advent-of-code.support/read-input 13 2)))
    "d14.p1" (println (advent-of-code.day-14/part-1 (advent-of-code.support/read-input 14 1)))
    "d14.p2" (println (advent-of-code.day-14/part-2 (advent-of-code.support/read-input 14 2)))
    "d15.p1" (println (advent-of-code.day-15/part-1 (advent-of-code.support/read-input 15 1)))
    "d15.p2" (println (advent-of-code.day-15/part-2 (advent-of-code.support/read-input 15 2)))
    "d16.p1" (println (advent-of-code.day-16/part-1 (advent-of-code.support/read-input 16 1)))
    "d16.p2" (println (advent-of-code.day-16/part-2 (advent-of-code.support/read-input 16 2)))
    "d17.p1" (println (advent-of-code.day-17/part-1 (advent-of-code.support/read-input 17 1)))
    "d17.p2" (println (advent-of-code.day-17/part-2 (advent-of-code.support/read-input 17 2)))
    "d18.p1" (println (advent-of-code.day-18/part-1 (advent-of-code.support/read-input 18 1)))
    "d18.p2" (println (advent-of-code.day-18/part-2 (advent-of-code.support/read-input 18 2)))
    "d19.p1" (println (advent-of-code.day-19/part-1 (advent-of-code.support/read-input 19 1)))
    "d19.p2" (println (advent-of-code.day-19/part-2 (advent-of-code.support/read-input 19 2)))
    "d20.p1" (println (advent-of-code.day-20/part-1 (advent-of-code.support/read-input 20 1)))
    "d20.p2" (println (advent-of-code.day-20/part-2 (advent-of-code.support/read-input 20 2)))
    "d21.p1" (println (advent-of-code.day-21/part-1 (advent-of-code.support/read-input 21 1)))
    "d21.p2" (println (advent-of-code.day-21/part-2 (advent-of-code.support/read-input 21 2)))
    "d22.p1" (println (advent-of-code.day-22/part-1 (advent-of-code.support/read-input 22 1)))
    "d22.p2" (println (advent-of-code.day-22/part-2 (advent-of-code.support/read-input 22 2)))
    "d23.p1" (println (advent-of-code.day-23/part-1 (advent-of-code.support/read-input 23 1)))
    "d23.p2" (println (advent-of-code.day-23/part-2 (advent-of-code.support/read-input 23 2)))
    "d24.p1" (println (advent-of-code.day-24/part-1 (advent-of-code.support/read-input 24 1)))
    "d24.p2" (println (advent-of-code.day-24/part-2 (advent-of-code.support/read-input 24 2)))
    "d25.p1" (println (advent-of-code.day-25/part-1 (advent-of-code.support/read-input 25 1)))
    "d25.p2" (println (advent-of-code.day-25/part-2 (advent-of-code.support/read-input 25 2)))
    (println "not found")))

