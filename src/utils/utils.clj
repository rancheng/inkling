(ns utils)

(defmacro do_ [& exprs] (list 'let (apply vector (mapcat #(list '_ %) exprs)) '_ ))

(defmacro def-
  "private version of def"
  [name & decls]
    (list* `def (with-meta name (assoc (meta name) :private true)) decls))

(defn dnew [name & args] 
  (clojure.lang.Reflector/invokeConstructor (resolve name) (to-array args))) 
  
(println "Utils")