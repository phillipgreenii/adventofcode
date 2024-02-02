(ns advent-of-code.day-19
  (:require [clojure.string :as str]))

(defrecord Rating [x m a s])

(defn parse-rating [line]
  (let [[matched x-str m-str a-str s-str]
          ;{x=1416,m=956,a=1806,s=486}
        (re-find #"^\{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)\}$" line)]
    (when matched
      (Rating.
       (Integer/parseInt x-str)
       (Integer/parseInt m-str)
       (Integer/parseInt a-str)
       (Integer/parseInt s-str)))))

(defprotocol Rule
  "Workflow rule"
  (evaluate-rule [this rating] "returns evaluation of rule"))

(defrecord StaticRule [result]
  Rule
  (evaluate-rule [this _] (:result this)))

(defrecord PredicateRule [predicate result]
  Rule
  (evaluate-rule [this rating] (when ((:predicate this) rating)
                                 (:result this))))
(defn parse-result [s]
  (case s
    "A" :accepted
    "R" :rejected
    s))

(defn parse-attribute [s]
  (case s
    "x" :x
    "m" :m
    "a" :a
    "s" :s))

(defn parse-sign [s]
  (case s
    "<" <
    ">" >))

(defn parse-predicate [s]
  (let [[matched attribute-str sign-str value-str]
            ;x>1416
        (re-find #"^([xmas])([<>])([0-9]+)" s)
        attribute (parse-attribute attribute-str)
        sign (parse-sign sign-str)
        value (Integer/parseInt value-str)]
    (when matched
      (fn [rating]
        (sign (attribute rating) value)))))

(defn parse-rule [line]
  (let [parts (str/split line #":")]
    (if (= 1 (count parts))
      (StaticRule. (parse-result (first parts)))
      (PredicateRule. (parse-predicate (first parts))
                      (parse-result (second parts))))))

(defrecord Workflow [name rules])

(defn parse-workflow [line]
  (let [[matched name rules-str]
            ;{x=1416,m=956,a=1806,s=486}
        (re-find #"^([a-z]+)\{([^}]+)\}$" line)]
    (when matched
      (Workflow. name (doall
                       (map parse-rule
                            (str/split rules-str #",")))))))

(defn evaluate-workflow [workflow rating]
  (first
   (remove nil?
           (map #(evaluate-rule % rating)
                (:rules workflow)))))

(defn parse-input [input]
  (let [all-lines (str/split-lines input)]
    (loop [workflows {}
           ratings []
           workflows-complete false
           current-line (first all-lines)
           remaining-lines (rest all-lines)]
      (cond
        (nil? current-line) [(doall workflows) (doall ratings)]
        (empty? current-line) (recur workflows
                                     ratings
                                     true
                                     (first remaining-lines)
                                     (rest remaining-lines))
        workflows-complete (recur workflows
                                  (conj ratings (parse-rating current-line))
                                  workflows-complete
                                  (first remaining-lines)
                                  (rest remaining-lines))
        :else (recur (conj workflows ((juxt :name identity)
                                      (parse-workflow current-line)))
                     ratings
                     workflows-complete
                     (first remaining-lines)
                     (rest remaining-lines))))))

(defn evalute-rating [workflows rating]
  (loop [wfid "in"]
    (let [evaluation (evaluate-workflow (workflows wfid) rating)]
      (if (or (= :accepted evaluation)
              (= :rejected evaluation))
        [rating evaluation]
        (recur evaluation)))))

(defn score-rating [rating]
  (reduce +
          ((juxt :x :m :a :s) rating)))

(defn part-1
  "Day 19 Part 1"
  [input]
  (let [[workflows ratings] (parse-input input)
        evals (doall (map #(evalute-rating workflows %) ratings))
        accepted-ratings (doall (map first
                                     (filter #(= :accepted (second %)) evals)))
        scores (map score-rating accepted-ratings)]

    ;; (prn "workflows" workflows)
    ;; (prn "ratings" ratings)
    ;; (prn "evals" evals)
    ;; (prn "accepted-ratings" accepted-ratings)
    ;; (prn "scores" scores)
    (reduce + scores)))

(defn part-2
  "Day 19 Part 2"
  [input]
  input)
