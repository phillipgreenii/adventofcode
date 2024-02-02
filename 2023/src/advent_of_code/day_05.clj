(ns advent-of-code.day-05
  (:require [clojure.string :as str]))


(defrecord Range [start length])
(defn new-range [start length]
  (Range. start length))

(defn range-partition
  "returns two ranges, the first is overlap of r1 and r2, the second is list of remaining of r1"
  [r1 r2]
  (let [r1-s (:start r1)
        r1-e (+ r1-s (:length r1) -1)
        r2-s (:start r2)
        r2-e (+ r2-s (:length r2) -1)]
    (cond
      ;; disjoint
      (or (< r1-e r2-s)
          (< r2-e r1-s)) [nil (seq [r1])]
      ;; ( () ) all of r2 in r1 (end sticking out)
      (and (< r1-s  r2-s)
           (< r2-e r1-e)) [r2
                           (seq [(new-range r1-s (- r2-s r1-s))
                                 (new-range (inc r2-e) (- r1-e r2-e))])]
      ;; (()) all of r1 in r2
      (<= r2-s r1-s r1-e r2-e) [r1
                                nil]
      ;; (() start of r1 is out, but rest is in r2
      (<= r1-s r2-s r1-e r2-e) [(new-range r2-s (inc (- r1-e r2-s)))
                                (seq [(new-range r1-s (- r2-s r1-s))])]
      ;; ()) end of r1 is out, but rest is in r2
      (<= r2-s r1-s r2-e r1-e) [(new-range r1-s (inc (- r2-e r1-s)))
                                (seq [(new-range (inc r2-e) (- r1-e r2-e))])]
      ;; FIXME
      :else nil)))

(defn range-coalesce [r1 r2]
  (let [r1-s (:start r1)
        r1-e (+ r1-s (:length r1) -1)
        r2-s (:start r2)
        r2-e (+ r2-s (:length r2) -1)]
    (if (or
         ;; overlapping
         (and
          (<= r1-s r2-s  r1-e)
          (<= r2-s r1-e r2-e))
         ;; touching
         (= (inc r1-e) r2-s)
         (= (inc r2-e) r1-s))
      ;; merge
      (seq [(new-range (min r1-s r2-s)
                       (inc (- (max r1-e r2-e) (min r1-s r2-s))))])
      ;; disjoint
      (seq [r1 r2]))))


(defrecord CategoryMapping [dest-range-start src-range-start range-length])
(defn new-category-mapping [dest-range-start src-range-start range-length]
  (CategoryMapping. dest-range-start, src-range-start range-length))

(defn cmpp-src-to-dest [category-mapping source-id]
  (when (<= (:src-range-start category-mapping)
            source-id
            (+ -1 (:src-range-start category-mapping) (:range-length category-mapping)))
    (+ (:dest-range-start category-mapping)
       (- source-id (:src-range-start category-mapping)))))

(defn cmpp-src-range-to-dest-range [category-mapping source-range]
  (let [mapping-as-range (new-range
                          (:src-range-start category-mapping)
                          (:range-length category-mapping))
        [in-map out-of-map] (range-partition
                             source-range
                             mapping-as-range)
        updated-range (if (nil? in-map)
                        nil
                        (let [source-offset (if (> (:start in-map) (:src-range-start category-mapping))
                                              (- (:start in-map) (:src-range-start category-mapping))
                                              0)]
                          (new-range (+ (:dest-range-start category-mapping)
                                        source-offset)
                                     (:length in-map))))]
    (seq [updated-range out-of-map])))

(defrecord CategoryMap [name mappings])
(defn new-category-map [name mappings]
  (CategoryMap. name mappings))

(defn cm-lookup [category-map source-id]
  (let [lookup-result (first
                       (filter #(not (nil? %))
                               (map #(cmpp-src-to-dest % source-id)
                                    (:mappings category-map))))]
    (or lookup-result source-id)))

(defn cm-lookup-ranges [category-map source-ranges]
  (let [mappings (:mappings category-map)]
    (loop [mapping (first mappings)
           remaining-mappings (rest mappings)
           transformed-ranges nil
           untransformed-ranges source-ranges]
      (if (nil? mapping)
        (let [ranges
              (remove nil?
                      (concat transformed-ranges untransformed-ranges))
                ;; )
              ]
          ;; TODO use range-coalesce to reduce
          (sort-by :start ranges))
        (let [transform-results (map #(cmpp-src-range-to-dest-range mapping %) untransformed-ranges)]
          (recur
           (first remaining-mappings)
           (rest remaining-mappings)
           (concat transformed-ranges
                   (map first transform-results))
           (apply concat (map second transform-results))))))))

(defn parse-single-seeds [line]
  (let [[_ number-string] (str/split line #":" 2)
        number-string-list (filter #(> (count %) 0) (str/split number-string #" "))
        seeds (map #(BigInteger. %) number-string-list)]
    seeds))

(defn parse-seed-ranges [line]
  (let [[_ number-string] (str/split line #":" 2)
        number-string-list (filter #(> (count %) 0) (str/split number-string #" "))
        seed-ranges (map #(apply new-range %)
                         (partition 2 (map #(BigInteger. %) number-string-list)))]
    seed-ranges))

(defn parse-category-maps [all-lines]
  (let [lines (drop-while str/blank? all-lines)] ;; skip initial blank lines
    (loop [cl (first lines)
           rl (rest lines)
           current-map-name nil
           current-mappings []
           category-maps {}]
      (if (nil? cl)
        (merge category-maps
               (hash-map current-map-name
                         (new-category-map current-map-name current-mappings)))
        (let [complete-map (= "" cl)
              start-map (str/ends-with? cl "map:")
              new-map-name (cond
                             complete-map nil
                             start-map (first (str/split cl #" " 2))
                             :else current-map-name)
              new-mappings (cond
                             complete-map []
                             start-map []
                             :else (conj current-mappings
                                         (apply new-category-mapping
                                                (map #(BigInteger. %) (str/split cl #" ")))))
              new-category-maps (cond
                                  complete-map (merge category-maps
                                                      (hash-map current-map-name
                                                                (new-category-map current-map-name current-mappings)))
                                  :else category-maps)]
          (recur (first rl)
                 (rest rl)
                 new-map-name
                 new-mappings
                 new-category-maps))))))

(defn parse-input [parse-seeds input]
  (let [lines (str/split-lines input)
        seeds (parse-seeds (first lines))
        category-maps (parse-category-maps (rest lines))]
    [seeds category-maps]))

(def path ["seed-to-soil"
           "soil-to-fertilizer"
           "fertilizer-to-water"
           "water-to-light"
           "light-to-temperature"
           "temperature-to-humidity"
           "humidity-to-location"])

(defn lookup-location [category-maps seed]
  (reduce (fn [source-id category-map-name]
            (cm-lookup
             (get category-maps category-map-name)
             source-id))
          seed
          path))

(defn parse-input-as-single-seeds [input]
  (parse-input parse-single-seeds input))

(defn part-1
  "Day 05 Part 1"
  [input]
  (let [[seeds category-maps] (parse-input-as-single-seeds input)
        locations (map #(lookup-location category-maps %) seeds)]
    (apply min locations)))

(defn parse-input-as-seed-ranges [input]
  (parse-input parse-seed-ranges input))

(defn lookup-location-ranges [category-maps seed-ranges]
  (reduce (fn [source-ranges category-map-name]
            (cm-lookup-ranges
             (get category-maps category-map-name)
             source-ranges))
          seed-ranges
          path))

(defn part-2
  "Day 05 Part 2"
  [input]
  (let [[seed-ranges category-maps] (parse-input-as-seed-ranges input)
        location-ranges (lookup-location-ranges category-maps seed-ranges)]
    (apply min (map :start location-ranges))))
