(ns advent-of-code.day-14
  (:require [clojure.string :as str]))

(defn parse-platform [input]
  (apply vector
         (map #(apply vector
                      (char-array %))
              (str/split-lines input))))

(defn transpose-grid [grid]
  (when (not (nil? grid))
    (apply vector
           (apply map vector grid))))

(defn print-grid [grid]
  (println
   (str/join "\n"
             (map str/join grid))))

(defn shift-forward [cells]
  (loop [shifted-cells []
         gaps 0
         current-cell (first cells)
         remaining-cells (rest cells)]
    (if (nil? current-cell)
      (concat shifted-cells (take gaps (repeat \.)))
      (recur
       (case current-cell
         \. shifted-cells
         \# (concat shifted-cells
                    (take gaps (repeat \.))
                    (vector \#))
         (concat shifted-cells (vector current-cell)))
       (case current-cell
         \. (inc gaps)
         \# 0
         gaps)
       (first remaining-cells)
       (rest remaining-cells)))))

(defn shift-backwards [cells]
  (reverse
   (shift-forward
    (reverse cells))))

(defn tilt-rows [platform shifter]
  (map shifter platform))

(defn tilt-cols [platform shifter]
  (transpose-grid
   (tilt-rows (transpose-grid platform)
              shifter)))

(defn tilt-platform-north [platform]
  (tilt-cols platform shift-forward))

(defn tilt-platform-west [platform]
  (tilt-rows platform shift-forward))

(defn tilt-platform-south [platform]
  (tilt-cols platform shift-backwards))

(defn tilt-platform-east [platform]
  (tilt-rows platform shift-backwards))


(defn calculate-north-load [platform]
  (let [total-size (count platform)]
    (reduce +
            (map-indexed (fn [r row]
                           (let [multiplier (- total-size r)
                                 number-of-rocks (count (filter #(= \O %) row))]
                             (* multiplier number-of-rocks))) platform))))

(defn part-1
  "Day 14 Part 1"
  [input]
  (let [platform (parse-platform input)
        tilted-platform (tilt-platform-north platform)
        total-load-on-north (calculate-north-load tilted-platform)]
    ;; (prn "p")
    ;; (print-grid platform)
    ;; (prn "tp")
    ;; (print-grid tilted-platform)
    total-load-on-north))

(defn find-repeat [platform shifts]
  (loop [counter 0
         offset 0
         current-platform platform
         current-shift (first shifts)
         remaining-shifts (rest shifts)
         seen #{}]
    (let [shifted-platform (current-shift current-platform)
          id [offset shifted-platform]]
      (if (contains? seen id)
        [counter offset shifted-platform]
        (recur (inc counter)
               (mod counter 4)
               shifted-platform
               (first remaining-shifts)
               (rest remaining-shifts)
               (conj seen id))))))

(defn part-2
  "Day 14 Part 2"
  [input]
  (let [platform (parse-platform input)
        tilts (cycle [tilt-platform-north
                      tilt-platform-west
                      tilt-platform-south
                      tilt-platform-east])
        [counter offset tilted-platform] (find-repeat platform tilts)

        tilts-to-perform 1000000000
        needed-offset (mod (- tilts-to-perform counter) 4)
        next-tilts (drop (inc offset) tilts)
        final-tilted-platform
        (loop [previous-o offset
               previous-tp tilted-platform
               t (first next-tilts)
               rt (rest next-tilts)]
          (if (= previous-o needed-offset)
            previous-tp
            (recur
             (mod (inc previous-o) 4)
             (t previous-tp)
             (first rt)
             (rest rt))))
        total-load-on-north (calculate-north-load final-tilted-platform)]
    (prn "c o" counter offset)
    (prn "no" needed-offset)
    ;; (print-grid platform)
    (prn "tp")
    (print-grid final-tilted-platform)
    total-load-on-north))
