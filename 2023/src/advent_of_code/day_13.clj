(ns advent-of-code.day-13
  (:require [clojure.string :as str]))

(defn make-grid [lines]
  (apply vector
         (map #(apply vector %)
              lines)))

(defn transpose-grid [grid]
  (when (not (nil? grid))
    (apply vector
           (apply map vector grid))))

(defn parse-input [input]
  (loop [lines (str/split-lines input)
         grids []]
    (if (empty? lines)
      grids
      (let [[chunk remaining-lines] (split-with not-empty lines)]
        (recur (rest remaining-lines)
               (conj grids (make-grid chunk)))))))

(defn count-steps-to-palindrome [cells]
  (let [half (quot (count cells) 2)
        first-half (take half cells)
        last-half (take-last half cells)]
    (count
     (filter false?
             (map = first-half
                  (reverse last-half))))))

(defn split-on-reflection-point [row point]
  ;; even
  ;; [a b c d e f]
  ;; 1 => [a b        ] (0 1)
  ;; 2 => [a b c d    ] (0 3)
  ;; 3 => [a b c d e f] (0 5)
  ;; 4 => [    c d e f] (2 5)
  ;; 5 => [        e f] (4 5)
  ;; less or equal than half length
  ;; take first n * 2
  ;; greater than half
  ;; take last (length -n) * 2
  ;; odd
  ;; [a b c d e]
  ;; 1 => [a b      ] (0 1)
  ;; 2 => [a b c d  ] (0 3)
  ;; 3 => [  b c d e] (1 4)
  ;; 4 => [      d e] (3 4)
  ;; same path as before

  (if (<= point (/ (count row)
                   2))
    (take (* 2 point)
          row)
    (take-last (* 2
                  (- (count row) point))
               row)))

(defn determine-steps-to-reflection-point [row point]
  (count-steps-to-palindrome
   (split-on-reflection-point row point)))

(defn find-line-of-reflection-column [number-of-smudges grid]
  ;; there could be multiple, but the question doesn't mention
  ;; how to resolve that, so assuming only 1 will be possible
  (let [pp2smudges
        (loop [total-pp2smudges (into {} (map #(vector % 0)
                                              (range 1 (count (first grid)))))
               current-row (first grid)
               remaining-rows (rest grid)]
          (cond
            (empty? total-pp2smudges) nil
            (nil? current-row)  total-pp2smudges
            :else (let [row-pp2smudges  (into {} (map #(hash-map %
                                                                 (determine-steps-to-reflection-point current-row %))
                                                      (keys total-pp2smudges)))
                  ;;  _ (prn "tp" total-pp2smudges)
                  ;;  _ (prn "rp" row-pp2smudges)
                        combined-pp2smudges (merge-with + total-pp2smudges row-pp2smudges)
                        remaining-points (into {}
                                               (filter #(<= (second %) number-of-smudges)
                                                       combined-pp2smudges))]
                    (recur remaining-points
                           (first remaining-rows)
                           (rest remaining-rows)))))
        answers-with-smudges  (map first
                                   (filter #(= (second %) number-of-smudges)
                                           pp2smudges))]
    (first answers-with-smudges)))

(defn score-grid [number-of-smudges grid]
  (if-let [c-pos (find-line-of-reflection-column
                  number-of-smudges
                  grid)]
    c-pos
    (if-let [r-pos (find-line-of-reflection-column
                    number-of-smudges
                    (transpose-grid grid))]
      (* 100 r-pos)
      nil)))

(defn part-1
  "Day 13 Part 1"
  [input]
  (let [grids (parse-input input)
        scores (map #(score-grid 0 %) grids)]
    ;; (prn "p1 scores" scores)
    (reduce + scores)))

(defn part-2
  "Day 13 Part 2"
  [input]
  (let [grids (parse-input input)
        scores (map #(score-grid 1 %) grids)]
    ;; (prn "p2 scores" scores)
    (reduce + scores)))
