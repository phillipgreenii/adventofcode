(ns advent-of-code.day-21
  (:require [clojure.string :as str]))

(defrecord Map [row-count column-count starting-point rocks])

(defn parse-map [input]
  (let [lines (remove nil?
                      (str/split-lines input))
        row-count (count lines)
        column-count (count (first lines))
        [starting-point rocks] (loop [r 0
                                      c 0
                                      current-line (first lines)
                                      remaining-lines (rest lines)
                                      starting-point nil
                                      rocks #{}]
                                 (cond
                                   (and (empty? current-line)
                                        (empty? remaining-lines)) [starting-point rocks]
                                   (empty? current-line) (recur (inc r)
                                                                0
                                                                (first remaining-lines)
                                                                (rest remaining-lines)
                                                                starting-point
                                                                rocks)
                                   :else (let [cell (first current-line)]
                                           (case cell
                                             \. (recur r (inc c) (rest current-line) remaining-lines starting-point rocks)
                                             \# (recur r (inc c) (rest current-line) remaining-lines starting-point (conj rocks [r c]))
                                             \S (recur r (inc c) (rest current-line) remaining-lines [r c] rocks)))))]
    (Map. row-count column-count starting-point rocks)))

(defn print-map [this-map locations]
  (let [l-set (set locations)
        all (str/join "\n"
                      (for [r (range (.row-count this-map))]
                        (apply str
                               (for [c (range (.column-count this-map))]
                                 (cond
                                   (= (.starting-point this-map) [r c]) \S
                                   (contains? (.rocks this-map)
                                              [r c]) \#
                                   (contains? l-set
                                              [r c]) \O
                                   :else \.)))))]
    (println all)))

(defn find-locations-in-steps [the-map steps]
  (letfn [(out-of-bounds? [[r c]]
            ;; (prn "oob" r c)
            (or (< r 0)
                (< c 0)
                (>= r (.row-count the-map))
                (>= c (.column-count the-map))))
          (find-neighbors [unavailable [r c]]
            ;; (prn "find" r c unavailable)
            (let [possible [[(inc r) c]
                            [(dec r) c]
                            [r (inc c)]
                            [r (dec c)]]
                  valid (remove #(or (out-of-bounds? %)
                                     (contains? unavailable %))
                                possible)]
              ;; (prn "possible" possible)
              ;; (prn "valid" valid)
              valid))
          (filter-for-steps [loc-dist-list]
            (let [step-mod (mod steps 2)]
              (filter #(and (<= (second %) steps)
                            (= step-mod (mod (second %) 2)))
                      loc-dist-list)))]
    (let [loc-dist-list (loop [pos-dist [(.starting-point the-map) 0]
                               to-check  []
                               unavailable (.rocks the-map)
                               locations nil]
      ;; (prn "l" pos-dist (count to-check) (count unavailable) (count locations))
      ;; (prn "to-check" to-check)
                          ;;  (prn "un" unavailable)
                          ;; (prn "l" locations)
                          (let [[pos dist] pos-dist]
                            (if
                             (nil? pos-dist)
                              locations
                              (let [too-far? (> dist steps)
                                    neighbors (if too-far?
                                                nil
                                                (find-neighbors unavailable pos))
                                    updated-to-check (if too-far?
                                                       to-check
                                                       (let [neighbor-dist-list (map #(vector % (inc dist))
                                                                                     neighbors)
                                                             combined (concat to-check neighbor-dist-list)]
                                    ;;  (prn "ndl" neighbor-dist-list)
                                    ;;  (prn "combined" combined)
                                                         combined))
                                    updated-locations (if too-far?
                                                        locations
                                                        (conj locations pos-dist))
                                    updated-unavailable (if too-far?
                                                          (conj unavailable pos)
                                                          (apply conj unavailable pos neighbors))]
                                (recur
                                 (first updated-to-check)
                                 (rest updated-to-check)
                                 updated-unavailable
                                 updated-locations)))))
          filtered-loc-dist-list (filter-for-steps loc-dist-list)]
      (map first filtered-loc-dist-list))))

(defn part-1
  "Day 21 Part 1"
  ([input] (part-1 input 64))
  ([input steps]
   (let [map (parse-map input)
        ;;  _ (prn "map" map)
         locations (find-locations-in-steps map steps)]
    ;;  (prn "locations" locations)
    ;;  (print-map map locations)
     (count locations))))

(defn part-2
  "Day 21 Part 2"
  [input]
  input)
