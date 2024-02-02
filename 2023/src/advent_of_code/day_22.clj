(ns advent-of-code.day-22
  (:require [clojure.string :as str]))

(defmacro timed [expr]
  (let [sym (= (type expr) clojure.lang.Symbol)]
    `(let [start# (. System (nanoTime))
           return# ~expr
           res# (if ~sym
                  (resolve '~expr)
                  (resolve (first '~expr)))]
       (prn (str "Timed "
                ;;  (:name 
                  ;; (meta 
                 ~sym
                 " a "
                 (first ~expr)
                 " b "
                 ~expr
                 " c "
                   res#
                  ;;  )
                        ;; )
                 ": " (/ (double (- (. System (nanoTime)) start#)) 1000000.0) " msecs"))
       return#)))

(defn generate-labels []
  (let [num-of-symbols 26
        letters (map #(char (+ 65 %))
                     (range num-of-symbols))]
    (letfn [(gen-next [slots]
              (loop [current-slot (first slots)
                     remaining-slots (rest slots)
                     completed-slots []]
                (if (nil? current-slot)
                  ;; example nil => "A"
                  (conj completed-slots letters)
                  (if (not-empty (rest current-slot))
                    ;; example "BA" => "BB"; only one slot changes
                    (apply conj
                           (conj completed-slots (rest current-slot))
                           remaining-slots)
                    ;; example "BZ" => "CA"; a reset and cascade
                    (recur
                     (first remaining-slots)
                     (rest remaining-slots)
                     (conj completed-slots letters))))))
            (format-slots [slots]
              (apply str
                     (reverse
                      (map first slots))))]
      (map format-slots
           (iterate gen-next
                    (gen-next nil))))))

(defrecord Brick [x y z])

(defmethod print-method Brick [brick writer]
  (let [w writer]
    (.write w "[")
    (.write w (str/join ","
                        ((juxt :x :y :z)
                         brick)))
    (.write w "]")))

(defn parse-brick [line]
  (let [parts (str/split line #"," 3)
        [x y z] (map #(Integer/parseInt %) parts)]
    (Brick. x y z)))

(defrecord BrickStack [label start end])

(defn make-brick-stack [label start-x start-y start-z end-x end-y end-z]
  (BrickStack. label
               (Brick. start-x start-y start-z)
               (Brick. end-x end-y end-z)))

(defmethod print-method BrickStack [brick-stack writer]
  (letfn [(range2string [start end]
            (if (= start end)
              (str start)
              (str start "-" end)))]
    (let [w writer]
      (.write w "[")
      (.write w (.label brick-stack))
      (.write w ";")
      (.write w (str/join ","
                          [(range2string (:x (.start brick-stack)) (:x (.end brick-stack)))
                           (range2string (:y (.start brick-stack)) (:y (.end brick-stack)))
                           (range2string (:z (.start brick-stack)) (:z (.end brick-stack)))]))
      (.write w "]"))))

(defn parse-brick-stack [label line]
  (let [parts (str/split line #"~" 2)]
    (BrickStack. label
                 (parse-brick (first parts))
                 (parse-brick (second parts)))))

(defn parse-brick-stacks [input]
  (sort-by #(vector (.z (.start %))
                    (.z (.start %)))
           (map parse-brick-stack
                (generate-labels)
                (remove nil? (str/split-lines input)))))

(defn slice-at [brick-stacks z]
  (filter #(<= (.z (.start %))
               z
               (.z (.end %)))
          brick-stacks))

(defn slice [brick-stacks]
  (if (empty? brick-stacks)
    nil
    (remove nil?
            (let [max-z (apply max
                               (map #(:z (.end %))
                                    brick-stacks))]
              (for [z (range max-z 0 -1)]
                (let [s         (slice-at brick-stacks z)]
                  (when s
                    [z s])))))))

(def counter-intersects (atom 0))

(defn intersects? [slice brick-stack]
  (swap! counter-intersects inc)
  (letfn [(overlaps [f a b]
            (or (or
                 (<= (f (.start a))
                     (f (.start b))
                     (f (.end a)))
                 (<= (f (.start a))
                     (f (.end b))
                     (f (.end a))))
                (or
                 (<= (f (.start b))
                     (f (.start a))
                     (f (.end b)))
                 (<= (f (.start b))
                     (f (.end a))
                     (f (.end b))))))]
    (true?
     (some #(and (overlaps (fn [s] (.x s)) % brick-stack)
                 (overlaps (fn [s] (.y s)) % brick-stack))
           slice))))

(defn shift-down [brick-stack shift-amount]
  ;; (prn "sd" brick-stack shift-amount)
  (if (= 0 shift-amount)
    brick-stack
    (BrickStack.
     (.label brick-stack)
     (Brick. (.x (.start brick-stack))
             (.y (.start brick-stack))
             (- (.z (.start brick-stack)) shift-amount))
     (Brick. (.x (.end brick-stack))
             (.y (.end brick-stack))
             (- (.z (.end brick-stack)) shift-amount)))))

(def counter-squish-into (atom 0))

(defn squish-into [brick-stacks brick-stack]
  ;; (println (java.time.LocalDateTime/now))
  (swap! counter-squish-into inc)
  ;; (prn "si" brick-stacks brick-stack)
  (let [shift-amount
        (let [all-slices (slice brick-stacks)]
          (loop [[n slice] (first all-slices)
                 remaining-slices (rest all-slices)]
            ;; (prn "xxxx" n slice)
            (if (nil? slice)
              ;; if no interections, then move all the way to the bottom
              (dec (.z (.start brick-stack)))
              (let [intersects (intersects? slice brick-stack)]
                (if intersects
                  (- (.z (.start brick-stack)) (inc n))
                  (recur
                   (first remaining-slices)
                   (rest remaining-slices)))))))]
    (concat brick-stacks
            [(shift-down brick-stack shift-amount)])))

(defn squish [brick-stacks]
  (cond
    (empty? brick-stacks) brick-stacks
    (= 1 (count brick-stacks)) (timed 
                                (squish-into nil
                                            (first brick-stacks)))
    :else (loop [squished-brick-stacks []
                 remaining-brick-stacks brick-stacks]
            (if (empty? remaining-brick-stacks)
              squished-brick-stacks
              (recur
               (timed (squish-into squished-brick-stacks
                            (first remaining-brick-stacks)))
               (rest remaining-brick-stacks))))))

(defn squishable? [brick-stacks]
  (not= brick-stacks
        (squish brick-stacks)))

(defn find-disintegratable-stacks [brick-stacks]
  (remove nil?
          (for [n (range (count brick-stacks))]
            (let [;; _ (prn "n" n)
                  parts (split-at n brick-stacks)
                  ;; _ (prn "parts" parts)
                  with-out-n (concat (first parts)
                                     (rest (second parts)))
                  ;; _ (prn "won" with-out-n)
                  s (squishable? with-out-n)
                  ;; _ (prn "s" s)
                  ]
              (when (not s)
                (nth brick-stacks n))))))

(defn part-1
  "Day 22 Part 1"
  [input]
  (let [brick-stacks (parse-brick-stacks input)
        squished-brick-stacks  (squish brick-stacks)
        ;; disintegratable-stacks (find-disintegratable-stacks squished-brick-stacks)
        ]
    ;; (println brick-stacks)
    (println (count brick-stacks))
    ;; (apply println squished-brick-stacks)
    ;; (println squished-brick-stacks)
    (println (count squished-brick-stacks))
    (println "counter-squish-into" @counter-squish-into)
    (println "counter-intersects" @counter-intersects)
    ;; (println disintegratable-stacks)
    ;; (count disintegratable-stacks)
    0
    ))

(defn part-2
  "Day 22 Part 2"
  [input]
  input)
