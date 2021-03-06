(ns utils)

(defmacro do_ [& exprs] (list 'let (apply vector (mapcat #(list '_ %) exprs)) '_ ))
(defmacro doto-this [obj & exprs] `(let [~'this ~obj] (doto ~obj ~@exprs))) 

(defmacro def-
  "private version of def"
  [name & decls]
    (list* `def (with-meta name (assoc (meta name) :private true)) decls))

(defn dnew [name & args] 
  (clojure.lang.Reflector/invokeConstructor (resolve name) (to-array args))) 

