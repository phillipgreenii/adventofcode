(ns advent-of-code.day-10
  (:require [clojure.string :as str]
            [clojure.set :as set]))

(defn make-grid [rows]
  (apply vector (map #(apply vector (char-array %)) rows)))

(defn map-grid-indexed [map-cell-fn  grid]
  (let [convert-row (fn [i row]
                      (apply vector
                             (map-indexed #(map-cell-fn [i %1] %2) row)))]
    (apply vector
           (map-indexed convert-row grid))))

(defn find-start [grid]
  (let [rows-with-indexes  (map-indexed vector grid)]
    (loop [i-r (first rows-with-indexes)
           remaining (rest rows-with-indexes)]
      (if (nil? i-r)
        nil
        (let [i (.indexOf (second i-r) \S)]
          (if (>= i 0)
            [(first i-r) i]
            (recur (first remaining)
                   (rest remaining))))))))

(defn find-incoming-connected-neighbors [grid [r c]]
  (let [connects? (fn [connections l]
                    (let [c (get-in grid [(first l) (second l)])]
                      (when (and (not (nil? c))
                                 (contains? connections
                                            c))
                        l)))
        up  [(dec r) c]
        down  [(inc r) c]
        left  [r (dec c)]
        right  [r (inc c)]
        connected-locations  [(connects? #{\| \7 \F} up)
                              (connects? #{\| \L \J} down)
                              (connects? #{\- \L \F} left)
                              (connects? #{\- \7 \J} right)]]
    (remove nil?
            connected-locations)))

(defn l-right [[r c]] [r (inc c)])
(defn l-left  [[r c]] [r (dec c)])
(defn l-up    [[r c]] [(dec r) c])
(defn l-down  [[r c]] [(inc r) c])

(defrecord PipeMaze [grid start])

(defn make-pipe-maze [grid]
  (let [start (find-start grid)
        translate-start (fn [pos]
                          (let [neighbors (find-incoming-connected-neighbors grid pos)
                                is-neighbor? (fn [[r c]]
                                               (<= 0 (.indexOf neighbors [r c])))
                                matches (fn [opt1 opt2]
                                          (every? is-neighbor?
                                                  ((juxt opt1 opt2) pos)))]
                            (cond
                              (matches l-down  l-up)    \|
                              (matches l-right l-left)  \-
                              (matches l-right l-down)  \F
                              (matches l-left  l-down)  \7
                              (matches l-left  l-up)    \J
                              (matches l-right l-up)    \L
                              :else \?)))
        updated-grid (map-grid-indexed (fn [pos x]
                                         (if (= pos start)
                                           (translate-start pos)
                                           x))
                                       grid)]
    (PipeMaze. updated-grid start)))

(defn find-outgoing-connected-neighbors [grid l]
  (let [max-r (dec (count grid))
        max-c (dec (count (first grid)))
        s (get-in grid l)
        possible-neighbors
        (case s
          \| [(l-up    l) (l-down l)]
          \- [(l-right l) (l-left l)]
          \7 [(l-left  l) (l-down l)]
          \F [(l-right l) (l-down l)]
          \L [(l-left  l) (l-up   l)]
          \J [(l-right l) (l-up   l)]
          [])
        filtered-neighbors
        (filter (fn [[nr nc]] (and (<= 0 nr max-r)
                                   (<= 0 nc max-c)))
                possible-neighbors)]
    filtered-neighbors))

(defn print-grid [grid]
  (println
   (str/join "\n"
             (map str/join grid))))

(defn overlay-grid [grid loop inside-spaces outside-spaces]
  (let [loop-as-set (set loop)
        outside-spaces-as-set (set outside-spaces)
        inside-spaces-as-set (set inside-spaces)
        convert (fn [[r c] x]
                  (cond (contains? loop-as-set [r c]) x
                        (contains? outside-spaces-as-set [r c]) \O
                        (contains? inside-spaces-as-set [r c]) \I
                        :else \.))]
    (map-grid-indexed convert grid)))

(defn find-loop [maze]
  (let [grid (:grid maze)]
    (loop [visited []
           current-location (:start maze)]
      (if (nil? current-location)
        visited
        (let [neighbors (find-outgoing-connected-neighbors grid current-location)
              next-location (first
                             (drop-while
                              #(<= 0 (.indexOf visited %))
                              neighbors))]
          (recur (conj visited current-location)
                 next-location))))))

(defn part-1
  "Day 10 Part 1"
  ;; FIXME this is broken, perhaps related to trying to make part 2 work (verify fails)
  [input]
  (let [grid (make-grid (str/split-lines input))
        maze (make-pipe-maze grid)
        loop (find-loop maze)]
    ;; max distance is half the total path
    (quot (count loop) 2)))

(defn find-edge [grid original-loop]
  ; TODO implement me
  )

(defn find-partitions [grid original-loop]
  ;; [x y] => x*1000 + y as comparison
  (let [up-corner (apply min-key #(+ (* (first %) 1000) (second %)) original-loop)
        offset (.indexOf original-loop up-corner)
        rotated-loop (concat (drop offset original-loop)
                             (take offset original-loop))
        second-loc (second rotated-loop)
        clockwise (or (= (l-up    up-corner) second-loc)
                      (= (l-right up-corner) second-loc))
        determine-direction (fn [current-pos next-pos]
                              (cond
                                (= (l-up    current-pos) next-pos) \U
                                (= (l-down  current-pos) next-pos) \D
                                (= (l-left  current-pos) next-pos) \L
                                (= (l-right current-pos) next-pos) \R
                                :else (throw (IllegalStateException. "Unable to determine direction"))))
        original-direction (determine-direction up-corner second-loc)
        ;; direction represent which way is inside or out
        ;; | true => inside right
        ;; - true => inside down
        ;; 7 true => inside (left/down)
        ;; J true => inside (left/up)
        ;; F true => inside (right/down)
        ;; L true => inside (right/up) 
        ;; starting-direction (if (not= x \F) (throw (IllegalStateException. "Upper left not 'F"))
        ;;                        true)
        [outside-edge inside-edge] (loop [current-space up-corner
                                          next-space second-loc
                                          direction original-direction
                                          remaining-spaces (rest (rest rotated-loop))
                                          outspaces #{}
                                          inspaces #{}]
                                     (if (nil? next-space)
                                       [outspaces inspaces]
                                       (let [next-next-space (first remaining-spaces)
                                             current-x (get-in grid current-space)
                                             ;; standard-in-out is like the "correct side of the hall to walk on"
                                             ;; one was chosen and we just need to know to use it or flip it
                                             standard-in-out (and clockwise
                                                                  (or (= direction \U)
                                                                      (= direction \R)))
                                             all-used-spaces (merge (set rotated-loop) outspaces inspaces)
                                             extract-spaces (fn [out-l in-l]
                                                              [(remove #(contains? all-used-spaces %) ((apply juxt out-l) current-space))
                                                               (remove #(contains? all-used-spaces %) ((apply juxt in-l) current-space))])
                                             [standard-out standard-in] (case direction
                                                                          ;; TODO this need finished or redone
                                                                          \| (extract-spaces [l-left] [l-right])
                                                                          \- (extract-spaces [l-up]   [l-down])
                                                                          \7 (extract-spaces []   [])
                                                                          \J (extract-spaces []   [])
                                                                          \F (extract-spaces []   [])
                                                                          \L (extract-spaces []   []))
                                             [additional-out-spaces additional-in-spaces] (if standard-in-out
                                                                                            [standard-out standard-in]
                                                                                            [standard-in standard-out])]
                                         (recur
                                          (determine-direction next-space next-next-space)
                                          next-space
                                          next-next-space
                                          (rest remaining-spaces)
                                          (merge outspaces additional-out-spaces)
                                          (merge inspaces additional-in-spaces)))))
        expand-spaces (fn [current-spaces & other-spaces]
                        (let [already-marked (apply set/union (map set other-spaces))]
                          (loop [current-space (first current-spaces)
                                 remaining-spaces (second current-spaces)
                                 spaces current-spaces]
                            (if (nil? current-space)
                              remaining-spaces
                              (recur (first remaining-spaces)
                                     (concat (rest remaining-spaces)
                                             (remove #(or (contains? already-marked %)
                                                          (contains? spaces %))
                                                     ((juxt l-up l-down l-right l-left) current-space)))
                                     (conj spaces current-space))))))
        inside-spaces (expand-spaces inside-edge rotated-loop)
        outside-spaces (expand-spaces outside-edge rotated-loop inside-spaces)]
    [outside-spaces inside-spaces]))


(defn part-2
  "Day 10 Part 2"
  [input]
  (let [grid (make-grid (str/split-lines input))
        maze (make-pipe-maze grid)
        loop (find-loop maze)
        [outside-spaces inside-spaces] (find-partitions grid loop)]
    (print-grid
     (overlay-grid (:grid maze) loop inside-spaces outside-spaces))
    (count inside-spaces)))

  ;; note
  ;; start with outside and expand out
  ;; loop through path to identify if outside or inside
  ;; alternative: start with upper left most position; figuire out what is outside
  ;; follow path, keeping track of inside vs outside
  ;; expand inside 
  ;; count inside
