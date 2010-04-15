(ns unit)

(defmacro ans [args & defs]
  `{:args ~args
    



  `(fn ~(vec args) 
      ~@defs)))

(defmacro eval-ans 
  ([template]
    `(~@(template :defs)))
  ([template name]
    `(let [old-ns# *ns*
           defs# (~template :defs)]
        (in-ns '~name) 
        (eval defs#)
;;         (in-ns (ns-name old-ns#))
        '~name)))

;; (defmacro lookup [ns sym]
;;   `(sym 