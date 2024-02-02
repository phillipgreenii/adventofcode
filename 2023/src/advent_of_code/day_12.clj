(ns advent-of-code.day-12
  (:require [clojure.string :as str]))

(defn parse-line [line]
  (let [[ticks-strs count-strs] (str/split line #" " 2)
        ticks (apply vector ticks-strs)
        counts (map #(Integer/parseInt %) (str/split count-strs #","))]
    [ticks counts]))

(defn is-valid-arragement [expected-counts ticks]
  (let [chunks (remove empty?
                       (str/split ticks #"[.]+"))
        counts (map count chunks)]
    ;; (prn "chunks" chunks)
    (= expected-counts counts)))

(defn generate-possible-arragements [ticks]
  ;; (prn "ticks" ticks)
  (letfn [(r [prev current remaining]
            ;;  (prn "r" prev "%%%%" current "%%%" remaining)
            (cond
              (nil? current) [(apply str prev)]
              (not=  \? current) (r (conj prev current)
                                    (first remaining)
                                    (rest remaining))
              :else (concat (r (conj prev \.)
                               (first remaining)
                               (rest remaining))
                            (r (conj prev \#)
                               (first remaining)
                               (rest remaining)))))]
    (r [] (first ticks) (rest ticks))))


(defn count-possible-arragements [[ticks counts]]
  (let [all-arragements (generate-possible-arragements ticks)
        valid-arragements (filter #(is-valid-arragement counts %)
                                  all-arragements)]
    ;; (prn "tc" ticks counts)
    ;; (prn "a" all-arragements)
    ;; (prn "v" valid-arragements)
    (count valid-arragements)))

(defn part-1
  "Day 12 Part 1"
  [input]
  (let [records (map parse-line (str/split-lines input))
        counts (map count-possible-arragements records)]
    (reduce + counts)))

(defn unfold-record [[ticks counts]]
  (let [uf-ticks  (apply vector
                         (str/join "?"
                                   (repeat 5
                                           (apply str ticks))))
        uf-counts (apply concat (repeat 5 counts))]
    [uf-ticks uf-counts]))

(defn part-2
  "Day 12 Part 2"
  [input]
  (let [records (map parse-line (str/split-lines input))
        unfolded-records (map unfold-record records)
        ;; TODO this should be unfolded-records, but the algorithm is not efficient enough to run yet
        counts (map count-possible-arragements records)
        ;; counts (map count-possible-arragements unfolded-records)
        ]
    (reduce + counts)))
