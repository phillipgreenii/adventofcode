(ns advent-of-code.day-17
  (:require [clojure.string :as str]))


(defn map-grid-indexed [map-cell-fn grid]
  (let [convert-row (fn [i row]
                      (apply vector
                             (map-indexed #(map-cell-fn [i %1] %2) row)))]
    (apply vector
           (map-indexed convert-row grid))))

(defn map-grid [map-cell-fn grid]
  (map-grid-indexed #(map-cell-fn %2) grid))

(defn parse-grid [input]
  (map-grid #(Character/digit % 10)
            (vec
             (map vec
                  (str/split-lines input)))))



(defn solve-min-heat-loss-path [grid start-point end-point]
  ;; (prn "solving " start-point end-point)
  (letfn [(build-neighbor [[r c] direction]
            (let [new-p (case direction
                          \< [r (dec c)]
                          \> [r (inc c)]
                          \^ [(dec r) c]
                          \v [(inc r) c])]
              [new-p direction (get-in grid new-p)]))
          (determine-neighbors [current-point direction]
            (cond-> []
              ; right
              (not= \< direction) (conj
                                   (build-neighbor current-point \>))
              ; left
              (not= \> direction) (conj
                                   (build-neighbor current-point \<))
              ; up
              (not= \v direction) (conj
                                   (build-neighbor current-point \^))
              ; down
              (not= \^ direction) (conj
                                   (build-neighbor current-point \v))))
          (find-best-option [options]
            (let [solved (first (filter (fn [[path heat-loss solved]]
                                          #(= true solved))
                                        options))]
              ;; (when solved 
              ;;   (prn "SOLVED!" solved))
              (if solved
                solved
                (min-key second options))))
          (solve [current-point direction visited repeated-direction-count total-heatloss]
                ;;  (when (>= total-heatloss 5000)
                ;;    (throw (IllegalStateException. "limit")))
            ;; (prn "solve" current-point (get-in grid current-point) direction "" repeated-direction-count total-heatloss
            ;;      (= current-point end-point)
            ;;      )
            (cond
              (nil? current-point) nil
              (= current-point end-point) [(seq [current-point])
                                           (+ total-heatloss
                                              (get-in grid current-point))
                                           true]
              :else (let [neighbors (determine-neighbors current-point direction)
                          valid-neighbors (remove (fn [[point new-direction heat-loss]]
                                                    (or
                                                     ;; invalid r c 
                                                     (nil? heat-loss)
                                                     ;; already been there
                                                     (contains? visited point)
                                                     ;; need to try a different direction
                                                     (and (= new-direction direction)
                                                          (= repeated-direction-count 3))))
                                                  neighbors)
                          options (remove nil?
                                          (map (fn [[point new-direction heat-loss]]
                                                 (solve point
                                                        new-direction
                                                        (conj visited current-point)
                                                        (if (= direction new-direction)
                                                          (inc repeated-direction-count)
                                                          1)
                                                        (+ total-heatloss heat-loss)))
                                               valid-neighbors))
                          best-option (find-best-option options)
                          [best-path best-heat-loss] best-option]
                      (if (nil? best-path)
                        nil
                        [(conj best-path current-point)  best-heat-loss]))))]
    (map first
         (solve start-point \> #{} 1 0))))

(defn part-1
  "Day 17 Part 1"
  [input]
  (let [grid (parse-grid input)
        start-point [0 0]
        end-point [(dec (count grid)) (dec (count (first grid)))]
        path (solve-min-heat-loss-path grid start-point end-point)]
    (count path)))

(defn part-2
  "Day 17 Part 2"
  [input]
  input)
