(ns advent-of-code.day-07
  (:require [clojure.string :as str]))

(defrecord Hand [val type sort-key bid])

(defn new-hand [val type sort-key bid]
  (Hand. val type sort-key bid))

(defn handle-jokers [card-counts]
  (if (or (= (count card-counts) 1)
          (not (contains? card-counts \X)))
    card-counts
    ;; 0 j same as original
    ;; 1 j high->onep onep->three twop->full three->four four->five    
    ;; 2 j high->three onep->four three->five
    ;; 3 j high->four onep->five
    ;; 4 j high->five
    ;; 5 j five
    ;; conclusion: always add j count to highest
    (let [jokers (get card-counts \X 0)
          counts-without-jokers (dissoc card-counts \X)
          most-card (first (apply max-key val counts-without-jokers))
          updated-card-counts (merge-with + counts-without-jokers (hash-map most-card jokers))]
      updated-card-counts)))

(defn calculate-type [val]
  ;; split and count, find highest and second highest numbers
  (let [original-counts (frequencies val)
        counts (handle-jokers original-counts)
        [high-1 high-2 & _] (reverse (sort (vals counts)))]
    (cond
      (= 5 high-1) [6 :five-of-kind]
      (= 4 high-1) [5 :four-of-kind]
      (and (= 3 high-1)
           (= 2 high-2)) [4 :full-house]
      (= 3 high-1) [3 :three-of-kind]
      (and (= 2 high-1)
           (= 2 high-2)) [2 :two-pair]
      (= 2 high-1) [1 :one-pair]
      :else [0 :high-card])))

(defn score-card [card]
  (case card
    \A 14
    \K 13
    \Q 12
    \J 11
    \T 10
    \X 1 ; joker
    (Integer/parseInt (str card))))

(defn build-sort-key [type val]
  (let [[type-score _] type
        card-scores (map score-card val)
        all-scores (conj card-scores type-score)
        ;; this converts (1 2 3 4 5 6) => 1020304050600
        sort-key  (reduce #(* 100 (+ %1  %2)) 0 all-scores)]
    sort-key))

(defn parse-hand [line]
  (let [[val bid-as-str] (str/split line #" " 2)
        bid (Integer/parseInt bid-as-str)
        type (calculate-type val)
        sort-key (build-sort-key type val)]
    (new-hand val type sort-key bid)))

(defn part-1
  "Day 07 Part 1"
  [input]
  (let [hands (map parse-hand (str/split-lines input))
        ;; sorted in asc so rank 1 is smallest and rank n is biggest
        sorted-hands (sort-by :sort-key hands)
        ranked-bids (map-indexed #(* (inc %1) (:bid %2)) sorted-hands)]
    (reduce + ranked-bids)))

(defn part-2
  "Day 07 Part 2"
  [input]
  (let [hands (map #(parse-hand
                     ;; replace J with X (make jacks into jokers)
                     (str/replace % #"J" "X"))
                   (str/split-lines input))
        ;; sorted in asc so rank 1 is smallest and rank n is biggest
        sorted-hands (sort-by :sort-key hands)
        ranked-bids (map-indexed #(* (inc %1) (:bid %2)) sorted-hands)]
    (reduce + ranked-bids)))
