(ns advent-of-code.day-18
  (:require [clojure.string :as str]))

(defrecord Trench [direction amount color])

(defn parse-trench [line]
  (let [[matched direction-str amount-str color] (re-find #"^([RLUD])\s+([0-9]+)\s+\((\#[a-f0-9]+)\)$" line)]
    (when matched
      (Trench. (first direction-str) (Integer/parseInt amount-str) color))))

(defn parse-dig-plan [input]
  (map parse-trench (str/split-lines input)))

(defn follow-dig-plan [dig-plan]
  (loop [current-position [0 0]
         current-trench-plan (first dig-plan)
         remaining-trench-plans (rest dig-plan)
         full-trench []]
    ;; (prn "cp" current-position)
    ;; (prn "ctp" current-trench-plan)
    ;; (prn "ft" full-trench)
    (if (nil? current-trench-plan)
      full-trench
      (let [[r c] current-position
            [direction amount] ((juxt :direction :amount) current-trench-plan)
            stepper (case direction
                      \U #(vector (- r %) c)
                      \D #(vector (+ r %) c)
                      \L #(vector r (- c %))
                      \R #(vector r (+ c %)))
            new-trench (map stepper (range 1 (inc amount)))]
        (recur (last new-trench)
               (first remaining-trench-plans)
               (rest remaining-trench-plans)
               (concat full-trench new-trench))))))

(defn dig-interior [trench]
  ;; find first and last excluding the starting corner
  (let [first-hole (first trench)
        last-hole (second (reverse trench))
        ;; right   down
        ;; [0  1] + [ 1 0]  == [ 1  1]
        ;; right   up
        ;; [0  1] + [-1 0]  == [-1  1]
        ;; left   down
        ;; [0 -1] + [ 1 0]  == [ 1 -1]
        ;; left   up
        ;; [0 -1] + [-1 0]  == [-1 -1]
        first-inner-corner [(+ (first first-hole)
                               (first last-hole))
                            (+ (second first-hole)
                               (second last-hole))]]
    (loop [lagoon (set trench)
           current-hole first-inner-corner
           remaining nil]
      (if (nil? current-hole)
        lagoon
        (let [[r c] current-hole
              all-neighbors [[(inc r) (inc c)]
                             [(inc r) c]
                             [(inc r) (dec c)]
                             [r (inc c)]
                             [r (dec c)]
                             [(dec r) (inc c)]
                             [(dec r) c]
                             [(dec r) (dec c)]]
              neighbors-to-check (remove #(or (nil? %)
                                              (contains? lagoon %))
                                         all-neighbors)
              updated-remaining (if (contains? lagoon current-hole)
                                  remaining
                                  (concat remaining neighbors-to-check))]
          (recur (conj lagoon current-hole)
                 (first updated-remaining)
                 (rest updated-remaining)))))))

(defn part-1
  "Day 18 Part 1"
  [input]
  (let [dig-plan (parse-dig-plan input)
        full-trench (follow-dig-plan dig-plan)
        full-lagoon (dig-interior full-trench)]
    ;; (prn "DP" dig-plan)
    ;; (prn "FT" full-trench)
    ;; (prn "FL" full-lagoon)
    (count full-lagoon)))

(defn part-2
  "Day 18 Part 2"
  [input]
  input)
