(ns advent-of-code.day-02
  (:require [clojure.string :as str]))

(defrecord Draw [cubes])

(defrecord Game [num draws])

(defn parse-cube [^String s]
  (let [[count color] (str/split (str/trim s) #" " 2)]
    [(str/trim color) (Integer/parseInt count)]))

(defn parse-draw [^String s]
  (let [cube-parts (str/split s #",")]
    (->Draw (into {}
                  (map parse-cube
                       cube-parts)))))

(defn parse-game [^String line]
  (let [[p1 p2] (str/split line #":" 2)
        [_ num] (str/split p1 #" ", 2)
        draw-parts (str/split p2 #";")]
    (->Game (Integer/parseInt num)
            (map parse-draw draw-parts))))

(defn draw-possible-with-bag? [bag ^Draw draw]
  (let [cubes (:cubes draw)
        all-keys (distinct (into (keys bag) (keys cubes)))]
    (every? #(>= (get bag % 0) (get cubes % 0))
            all-keys)))

(defn game-possible-with-bag? [bag ^Game game]
  (every? #(draw-possible-with-bag? bag %)
          (:draws game)))

(defn part-1
  "Day 02 Part 1"
  [input]
  (let [games (map parse-game (str/split-lines input))
        bag (hash-map "red" 12 "green" 13 "blue" 14)
        possible-with-bag (filter
                           #(game-possible-with-bag? bag %)
                           games)]
    (apply + (map :num possible-with-bag))))

(defn find-min-bag [^Game game]
  (let [all-cubes (map :cubes  (flatten (:draws game)))
        min-bag (apply (partial merge-with max) all-cubes)]
    min-bag))

(defn part-2
  "Day 02 Part 2"
  [input]
  (let [games (map parse-game (str/split-lines input))]
    (apply +
           (map #(apply * (vals (find-min-bag %)))
                games))))
