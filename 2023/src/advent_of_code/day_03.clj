(ns advent-of-code.day-03
  (:require [clojure.string :as str]))

(defrecord Sym [value row col]
  Object
  (toString [_] (str "{" value ":" row "," col "}")))

(defn new-sym [value row col]
  (Sym. value row col))

(defrecord Num [value row col-start col-end]
  Object
  (toString [_] (str "{" value ":" row "," col-start "-" col-end "}")))

(defn new-num [value row col-start col-end]
  (Num. value row col-start col-end))

(defn extract-number-from-row [row line]
  (let [create-num (fn [start end] (Num. (Integer/parseInt (subs line start (inc end))) row start end))
        end (count line)]
    (loop [i 0
           num-start-i -1
           numbers []]
      (let [c (get line i)
            is-digit (and c (Character/isDigit c))
            current-num (not= num-start-i -1)
            num-just-ended (and (not is-digit) current-num)]
        (if (>= i end)
          (seq (if num-just-ended
                 (conj numbers (create-num num-start-i (dec end)))
                 numbers))
          (recur (inc i)
                 ;; calc num-start-i
                 (cond
                   (and is-digit (not current-num)) i
                   (and is-digit current-num) num-start-i
                   :else -1)
                 ;; calc numbers
                 (if num-just-ended
                   (conj numbers (create-num  num-start-i  (dec i)))
                   numbers)))))))

(defn is-symbol? [c]
  (not (or (nil? c)
           (Character/isDigit c)
           (= \. c))))

(def ^:const around-offsets
  ['(1 1)
   '(1 0)
   '(1 -1)
   '(-1 1)
   '(-1 0)
   '(-1 -1)
   '(0 1)
   '(0 -1)])

(defn extract-numbers [lines]
  (flatten
   (map-indexed #(extract-number-from-row  %1 %2)
                lines)))

(defn next-to? [sym num]
  (boolean
   (first (filter boolean
                  (for [offset around-offsets]
                    (let [r (+ (first offset) (:row sym))
                          c (+ (second offset) (:col sym))
                          n (and (= r (:row num))
                                 (<= (:col-start num) c (:col-end num)))]
                      n))))))

(defn is-part-number? [number syms]
  (some #(next-to? % number) syms))

(defn locate-symbols [grid]
  (remove nil?
          (for [r (range 0 (alength grid))
                c (range 0 (alength (aget grid 0)))]
            (let [x (aget grid r c)]
              (when (is-symbol? x)
                (new-sym x r c))))))

(defn part-1
  "Day 03 Part 1"
  [input]
  (let [lines (str/split-lines input)
        all-numbers (remove nil? (extract-numbers lines))
        grid (to-array-2d lines)
        all-syms (locate-symbols grid)
        part-numbers (filter #(is-part-number?  % all-syms) all-numbers)]
    (reduce + (map :value part-numbers))))

(defn part-2
  "Day 03 Part 2"
  [input]
  (let [lines (str/split-lines input)
        all-numbers (remove nil? (extract-numbers lines))
        grid (to-array-2d lines)
        all-syms (locate-symbols grid)
        potential-gears (filter #(= \* (:value %))  all-syms)
        gear-ratios (remove nil? (for [gear potential-gears]
                                   (let [n-list (filter #(next-to? gear %) all-numbers)]
                                     (when (> (count n-list) 1)
                                       (reduce * (map :value n-list))))))]
    (reduce + gear-ratios)))
