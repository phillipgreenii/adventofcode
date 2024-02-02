(ns advent-of-code.day-08
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defn parse-node [line]
  (let [[matched id left right] (re-find #"^([A-Z0-9]+)[^A-Z0-9]+([A-Z0-9]+)[^A-Z0-9]+([A-Z0-9]+)[^A-Z0-9]+$" line)]
    (when matched
      [id [left right]])))

(defn parse-input [input]
  (let [lines (str/split-lines input)
        directions (first lines)
        nodes  (map parse-node (remove #(= 0 (count %)) (rest lines)))
        nodes-map (apply hash-map (apply concat nodes))]
    [directions nodes-map]))

(defrecord PathSegment [starting-node starting-offset-mod ending-node ending-offset-mod total-steps])

(defn new-path-segment [starting-node starting-offset-mod ending-node ending-offset-mod total-steps]
  (PathSegment. starting-node starting-offset-mod ending-node ending-offset-mod total-steps))

(defn generate-path-segment-key [path-segment]
  (str/join "-"
            (map str
                 ((juxt :starting-node :starting-offset-mod :ending-node :ending-offset-mod :total-steps)
                  path-segment))))

(defn find-path-segment [directions nodes-map starting-node starting-offset]
  (let [m (fn [offset] (mod offset (count directions)))]
    (loop [first-time? true
           current-node starting-node
           current-offset starting-offset]
      (if (and (not first-time?)
               (str/ends-with? current-node "Z"))
        [current-node current-offset]
        (let [direction   (get directions (m current-offset))
              move-in-direction (if (= \L direction) first second)
              new-node (move-in-direction (get nodes-map current-node))]
          (recur  false
                  new-node
                  (inc current-offset)))))))

(defn find-path-loop [directions nodes-map starting-node]
  (let [m (fn [offset] (mod offset (count directions)))]
    (loop [current-node starting-node
           current-offset 0
           path-segments []
           seen-path-segments #{}
           done? false]
      (if (or done? (> current-offset 10))
        path-segments
        (let [[ending-node ending-offset] (find-path-segment
                                           directions nodes-map
                                           current-node current-offset)
              path-segment (new-path-segment current-node (m current-offset)
                                             ending-node (m ending-offset)
                                             (- ending-offset current-offset))
              path-segment-key (generate-path-segment-key path-segment)
              loop-complete (contains? seen-path-segments path-segment-key)]
          (recur ending-node
                 ending-offset
                 (if loop-complete
                   path-segments
                   (conj path-segments path-segment))
                 (set/union seen-path-segments (set  [path-segment]))
                 loop-complete))))))

(defn gcd [a b]
  (loop [a a, b b]
    (if (= a 0)
      b
      (recur (mod b a)
             a))))

(defn lcm  [a b]
  (* b
     (quot a (gcd a b))))

(defn sum-seq
  ([s] (sum-seq s 0))
  ([s t] (cons t
               (lazy-seq
                (sum-seq (rest s)
                         (+ t (first s)))))))

(defn make-ghost [path-segment]
  (let [steps (map :total-steps path-segment)
        isteps (cycle steps)]
    ; because we can drop the first 0
    (rest
     (sum-seq isteps))))

(defn ghost-walk [initial-ghosts]
  (loop [ghosts initial-ghosts]
    (let [ghost-step-count (map first ghosts)
          mc (apply max ghost-step-count)]
      (if (apply = ghost-step-count)
        mc
        (recur (map (fn [g]
                      (drop-while #(< % mc) g))
                    ghosts))))))

(defn solve [directions nodes-map starting-nodes]
  (let [path-loops (map #(find-path-loop directions nodes-map %)
                        starting-nodes)]
    (cond
      ;; if only one node, then take the first path from it
      (= (count path-loops) 1)
      (:total-steps (first
                     (first path-loops)))
      ;; if all loops have a single segment, then LCM
      (every? #(= (count %) 1) path-loops)
      (reduce lcm (map #(:total-steps (first %))
                       path-loops))
      ;; ghost walk works, but not efficient, but no other cleaver solution 
      ;; was written for if multiple paths have multiple loops
      :else (ghost-walk (map make-ghost path-loops)))))

(defn part-1
  "Day 08 Part 1"
  [input]
  (let [[directions nodes-map] (parse-input input)
        starting-nodes ["AAA"]]
    (solve directions nodes-map starting-nodes)))

(defn part-2
  "Day 08 Part 2"
  [input]
  (let [[directions nodes-map] (parse-input input)
        starting-nodes (filter #(str/ends-with? % "A") (keys nodes-map))]
    (solve directions nodes-map starting-nodes)))
