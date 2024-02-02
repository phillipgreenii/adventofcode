(ns advent-of-code.day-20
  (:require [clojure.set :as set]
            [clojure.string :as str]))

(defrecord Pulse [level src dest])
(defn make-pulse [level src dest]
  (Pulse. level src dest))
(defn make-high-pulse [src dest]
  (Pulse. :high src dest))
(defn make-low-pulse [src dest]
  (Pulse. :low src dest))

(defprotocol CommunicationModule
  "Communication module for machines"
  (receive [this pulse] "handles the incoming pulse and will return a list output pulses"))


(deftype FlipFlop [name destinations
                    ; TODO what is the more clojure way of handing this internal update?
                   ^:unsynchronized-mutable on?]
  CommunicationModule
  (receive [_ pulse]
    (if (= :high (:level pulse))
     ; high -> noop 
      nil
      (if on?
        ; on + low -> off + low
        (do
          (set! on? false)
          (map #(make-low-pulse name %) destinations))
        ; off + low -> on + high
        (do
          (set! on? true)
          (map #(make-high-pulse name %) destinations))))))

(defn make-flip-flop [name destinations]
  (FlipFlop. name destinations false))

(defmethod print-method FlipFlop [flip-flop writer]
  (let [w writer]
    (.write w "@flip-flop")
    (.write w " \"")
    (.write w (.name flip-flop))
    (.write w "\" ")
    (.write w "->[")
    (.write w (str/join "," (.destinations flip-flop)))
    (.write w "]")))

(deftype Conjunction [name incoming-modules destinations
                    ; TODO what is the more clojure way of handing this internal update?
                      ^:unsynchronized-mutable last-seen-pulses]
  CommunicationModule
  (receive [_ pulse]
    (set! last-seen-pulses
          (assoc-in last-seen-pulses [(:src pulse)] (:level pulse)))
    (let [level-to-send (if (every? #(= :high %) (vals last-seen-pulses))
                          :low
                          :high)]
      (map #(make-pulse level-to-send name %) destinations))))


(defn make-conjunction [name incoming-modules destinations]
  (Conjunction. name incoming-modules destinations
                (into {}
                      (map #(vector % :low) incoming-modules))))

(defmethod print-method Conjunction [conjunction writer]
  (let [w writer]
    (.write w "@conjunction")
    (.write w " \"")
    (.write w (.name conjunction))
    (.write w "\" ")
    (.write w "<-[")
    (.write w (str/join "," (.incoming-modules conjunction)))
    (.write w "]")
    (.write w "->[")
    (.write w (str/join "," (.destinations conjunction)))
    (.write w "]")))

(deftype Broadcaster [destinations]
  CommunicationModule
  (receive [_ pulse]
    (let [level-to-send (:level pulse)]
      (map #(make-pulse level-to-send "broadcaster" %) destinations))))

(defn make-broadcaster [destinations]
  (Broadcaster. destinations))

(defmethod print-method Broadcaster [broadcaster writer]
  (let [w writer]
    (.write w "@broadcaster")
    (.write w "->[")
    (.write w (str/join "," (.destinations broadcaster)))
    (.write w "]")))

(deftype Output [name]
  CommunicationModule
  (receive [_ pulse]
    ;; (prn "output" name "received" pulse)
    nil))

(defn make-output [name]
  (Output. name))

(defmethod print-method Output [output writer]
  (doto writer
    (.write "@output")
    (.write " \"")
    (.write (.name output))
    (.write "\"")))

(defn parse-modules [input]
  (letfn [(parse-info [s]
            (let [[matched type-str name destinations-str]
                                ;%a -> b
                  (re-find #"^([%&]?)([a-z]+) -> (.*)$" s)]
              (when matched
                [; type
                 (case type-str
                   "%" :flip-flop
                   "&" :conjunction
                   :broadcaster)
                 ; name
                 name
                 ;destinations
                 (map str/trim
                      (str/split destinations-str #","))])))]
    (let [infos (map parse-info
                     (remove nil?
                             (str/split-lines input)))
          ; this will be a hash map where key is a module and the value is the names of
          ;  modules which send it pulses
          upstream-lookup (apply merge-with concat
                                 (map (fn [[_ name destinations]]
                                        (into {}
                                              (map #(vector % [name]) destinations)))
                                      infos))
          untyped-modules (set/difference (set (keys upstream-lookup))
                                          (set (map second infos)))
          output-infos (map #(vector :output % nil) untyped-modules)
          all-infos (concat infos output-infos)]
      (into {}
            (map (fn [[type name destinations]]
                   [name
                    (case type
                      :flip-flop (make-flip-flop name destinations)
                      :conjunction (make-conjunction name (get upstream-lookup name) destinations)
                      :broadcaster (make-broadcaster destinations)
                      :output (make-output name))])
                 all-infos)))))

(defn push-button [modules]
  (let [button-pulse (make-low-pulse "button" "broadcaster")]
    (loop [pulses [button-pulse]
           high-pulse-count 0
           low-pulse-count 0]
      ;; (prn "pulses" pulses)
      (if (empty? pulses)
        {:high high-pulse-count :low low-pulse-count}
        (let [current-pulse (first pulses)
              pulse-level (:level current-pulse)
              ;; _ (prn "pulse" current-pulse)
              ;; _ (prn "dest" (:dest current-pulse))
              receiver (get modules (:dest current-pulse))
              new-pulses (receive receiver current-pulse)]
          (recur (concat (rest pulses)
                         new-pulses)
                 (if (= :high pulse-level)
                   (inc high-pulse-count)
                   high-pulse-count)
                 (if (= :low pulse-level)
                   (inc low-pulse-count)
                   low-pulse-count)))))))

(defn run-modules [modules times]
  (apply merge-with +
         (repeatedly times #(push-button modules))))

(defn part-1
  "Day 20 Part 1"
  [input]
  (let [modules (parse-modules input)
        ;; _ (prn "modules")
        ;; _ (run! prn modules)
        {high-pulse-count :high
         low-pulse-count :low} (run-modules modules 1000)]
    ;; (prn "high/low" high-pulse-count "/" low-pulse-count)
    (* high-pulse-count low-pulse-count)))

(defn part-2
  "Day 20 Part 2"
  [input]
  input)
