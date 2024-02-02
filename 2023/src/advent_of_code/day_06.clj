(ns advent-of-code.day-06
  (:require [clojure.string :as str]))

(defn parse-numbers [line]
  (map #(Integer/parseInt %)
       (rest
        (str/split line #"[ ]+"))))

(defn count-ways-to-win [record-time distance]
  ;; h = hold time
  ;; t = record-time - h
  ;; v = h * 1
  ;; 
  ;; d = t * v
  ;; d = (record-time - h) * h
  ;; h^2 - record-time*h + d = 0
  ;; for this problem, this is a parabolla with open side pointing down
  ;; if we use distance of d, this will find the sides and everything 
  ;; between will be the record
  ;; quadratic formula:
  ;; a = 1
  ;; b = -record-time
  ;; c = distance
  ;; h = (record-time [+/-] sqrt(record-time^2 - 4*1*distance)) / (2*1)
  (let [calc-d (fn [h] (* (- record-time h) h))
        sqrt_ans         (Math/sqrt (-
                                     (* record-time record-time)
                                     (* 4 distance)))
        h-lower-bound-double (/
                              (- record-time sqrt_ans)
                              2)
        h-upper-bound-double (/
                              (+ record-time sqrt_ans)
                              2)
        ;; round up because we want int which are between lower and upper
        h-lower-bound-rounded  (int (Math/ceil h-lower-bound-double))
        h-lower-bound (if (<= (calc-d h-lower-bound-rounded) distance)
                        (inc h-lower-bound-rounded)
                        h-lower-bound-rounded)
        ;; round down because we want int which are between lower and upper
        h-upper-bound-rounded  (int (Math/floor h-upper-bound-double))
        h-upper-bound (if (<= (calc-d h-upper-bound-rounded) distance)
                        (dec h-upper-bound-rounded)
                        h-upper-bound-rounded)]
    (inc (- h-upper-bound h-lower-bound))))

(defn part-1
  "Day 06 Part 1"
  [input]
  (let [[time-line distance-line & _] (str/split-lines input)
        times (parse-numbers time-line)
        distances (parse-numbers distance-line)
        race-records (map #(vector %1 %2) times distances)
        ways-to-win (map #(apply count-ways-to-win %) race-records)]
    (reduce * ways-to-win)))

(defn fix-kerning [numbers]
  (BigInteger.
   (apply str numbers)))

(defn part-2
  "Day 06 Part 2"
  [input]
  (let [[time-line distance-line & _] (str/split-lines input)
        time (fix-kerning (parse-numbers time-line))
        distance (fix-kerning (parse-numbers distance-line))
        ways-to-win (count-ways-to-win time distance)]
    ways-to-win))
