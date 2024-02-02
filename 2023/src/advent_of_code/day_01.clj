(ns advent-of-code.day-01
  (:require [clojure.string :as str]))


(defn translate-digit [^String d]
  (case d
    "one" 1
    "two" 2
    "three" 3
    "four" 4
    "five" 5
    "six" 6
    "seven" 7
    "eight" 8
    "nine" 9
    (Integer/parseInt d)))

(defn solve [^String input
             ^java.util.regex.Matcher digit-regex
             ^java.util.regex.Matcher rdigit-regex]
  (reduce +
          (map (fn [^String line]
                 (let [f (translate-digit
                          (re-find digit-regex line))
                       l (translate-digit
                          (str/reverse
                           (re-find rdigit-regex (str/reverse line))))
                       c (Integer/parseInt  (str f l))]
                   c))
               (str/split-lines input))))

(defn part-1
  "Day 01 Part 1"
  [input]
  (solve input #"\d" #"\d"))


(defn part-2
  "Day 01 Part 2"
  [input]
  (solve input #"\d|one|two|three|four|five|six|seven|eight|nine"  #"\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin"))
