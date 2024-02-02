(ns advent-of-code.support)

(defn read-input
  [day part]
  (let [file-path (first 
                    (remove nil? [
                      (clojure.java.io/resource 
                      (format "day%02d/part%d-input.private.txt" day part))           
                    
                      (clojure.java.io/resource 
                      (format "day%02d/input.private.txt" day))
                    ]
                    )
  
  )]
  (slurp file-path)))

(defn read-file
  [day name]
  (slurp (clojure.java.io/resource 
  (format "day%02d/%s.private.txt" day name)
  )))
