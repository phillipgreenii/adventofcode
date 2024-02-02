(ns advent-of-code.day-15
  (:require [clojure.string :as str]))

(defn parse-str-steps [input]
  (let [line (str/join "" (str/split-lines input))
        steps (str/split line #",")]
    steps))

(defn HASH [s]
  (reduce (fn [h c]
            (let [a (int c)]
              (mod (* (+ h a)
                      17)
                   256)))
          0
          s))

(defn part-1
  "Day 15 Part 1"
  [input]
  (let [str-steps (parse-str-steps input)
        hashes (map HASH str-steps)]
    (reduce + hashes)))

(defrecord Step [label operation focal-length hash])

(defn make-step [label operation focal-length]
  (Step. label operation focal-length (HASH label)))

(defn parse-step [str-step]
  (let [[matched label operation focal-length-str] (re-find #"^([A-Za-z]+)([=-])([0-9]?)$" str-step)]
    (when matched
      (make-step label operation (when (not= "" focal-length-str)
                                   (Integer/parseInt focal-length-str))))))

(defn print-step [step]
  (let [parts ((juxt :label :operation :focal-length)
               step)
        nnparts (remove nil? parts)]
    (prn
     (str/join "" (map str nnparts)))))

(defrecord Slot [label focal-length])

(defn make-slot [label focal-length]
  (Slot. label focal-length))

(defn make-slot-from-step [step]
  (make-slot (:label step) (:focal-length step)))

(defn merge-slots [slots step]
  (if (nil? slots) (seq [(make-slot-from-step step)])
      (let [new-slot (make-slot-from-step step)
            updated-slots (map #(if (= (:label %)
                                       (:label new-slot))
                                  new-slot
                                  %)
                               slots)]
        (if (not= slots updated-slots)
          updated-slots
          (concat slots [new-slot])))))

(defn slot-to-str [slot]
  (print-str "[" (:label slot) (:focal-length slot) "]"))

(defn slots-to-str [slots]
  (str/join " " (map slot-to-str slots)))

(defn apply-step-to-box [slots step]
  (case (:operation step)
    "-" (remove #(= (:label %) (:label step)) slots)
    "=" (merge-slots slots step)
    slots))

(defn apply-step-to-boxes [boxes step]
  (let [index (:hash step)
        box (get boxes index)
        updated-box (apply-step-to-box box step)]
    (assoc boxes index updated-box)))

(defn score-slots [slots]
  (reduce + 0 (map-indexed
               #(* (inc %1) (:focal-length %2))
               slots)))

(defn score-box [box]
  (if (nil? box)
    0
    (score-slots box)))

(defn score-boxes [boxes]
  (reduce +
          (map-indexed #(* (inc %1)
                           (score-box %2))
                       boxes)))

(defn print-boxes [boxes]
  (println
   (str/join "\n"
             (remove nil?
                     (map-indexed #(when (seq %2)
                                     (str "Box " %1 ": " (slots-to-str %2)))
                                  boxes)))))

(defn part-2
  "Day 15 Part 2"
  [input]
  (let [steps ;(take 5000
        (map parse-step (parse-str-steps input))
       ; )
        _ (prn "count" (count steps))
        boxes (reduce #(let [x (apply-step-to-boxes %1 %2)]
                        ;;  (print-step %2)
                        ;;  (print-boxes x)
                         x)
                      (vec (repeat 256 nil))
                      steps)
        score (score-boxes boxes)]
    score))
