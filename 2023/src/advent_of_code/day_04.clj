(ns advent-of-code.day-04
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defrecord Card [winning-numbers selected-numbers match-count])

(defn new-card [winning-numbers selected-numbers match-count]
  (Card. winning-numbers selected-numbers match-count))

(defn parse-numbers [^String number-string]
  (let [str-list (remove #(or (nil? %) (= "" %)) (str/split (str/trim number-string) #" "))]
    (map #(Integer/parseInt (str/trim %)) str-list)))

(defn count-matches [winning-numbers selected-numbers]
  (- (count winning-numbers)
     (count
      (set/difference  winning-numbers
                       selected-numbers))))

(defn parse-card [^String line]
  (let [[_ part2] (str/split line #":")
        [win-part selected-part] (str/split part2 #"\|")
        winning-numbers (set (parse-numbers win-part))
        selected-numbers (set (parse-numbers selected-part))]
    (new-card winning-numbers  selected-numbers
              (count-matches winning-numbers selected-numbers))))

(defn score-card [card]
  (let [match-count (:match-count card)]
    (if (= match-count 0) 0
        (int (Math/pow 2 (dec match-count))))))

(defn part-1
  "Day 04 Part 1"
  [input]
  (let [cards (map parse-card (str/split-lines input))
        scores (map score-card cards)]
    (reduce + scores)))

(defn part-2
  "Day 04 Part 2"
  [input]
  (let [cards (map parse-card (str/split-lines input))
        initial-remaining (into (hash-map) (map #(vector % 1) (range 1 (inc (count cards)))))]
    (loop [cn 1
           cc (first cards)
           rc (rest cards)
           remaining initial-remaining
           total-cards 0]
      (if (nil? cc) total-cards
          (let [num-to-create (get remaining cn)
                copied-cards  (range (inc cn)
                                     (+ 1 cn (:match-count cc)))
                additions (into (hash-map)
                                (map #(vector % num-to-create)
                                     copied-cards))
                removals (hash-map cn (- num-to-create))
                updated-remaining (merge-with + remaining additions removals)
                updated-total (+ total-cards num-to-create)]
            (recur (inc cn)
                   (first rc)
                   (rest rc)
                   updated-remaining
                   updated-total))))))

