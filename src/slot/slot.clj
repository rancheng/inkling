; A collection of utilities for using Qt's signal/slot mechanism within clojure

(in-ns 'slot)
(clojure/refer 'clojure)

(load-file "/home/jamie/inkling/src/utils.clj") (refer 'utils)

(import '(com.trolltech.qt QSignalEmitter
                           QSignalEmitter$Signal0
                           QSignalEmitter$Signal1
                           QSignalEmitter$Signal2
                           QSignalEmitter$Signal3
                           QSignalEmitter$Signal4
                           QSignalEmitter$Signal5
                           QSignalEmitter$Signal6
                           QSignalEmitter$Signal7
                           QSignalEmitter$Signal8
                           QSignalEmitter$Signal9)
        '(com.trolltech.qt.clojure QHolder
                                   QHolder$QSignalHolder0
                                   QHolder$QSignalHolder1
                                   QHolder$QSignalHolder2
                                   QHolder$QSignalHolder3
                                   QHolder$QSignalHolder4
                                   QHolder$QSignalHolder5
                                   QHolder$QSignalHolder6
                                   QHolder$QSignalHolder7
                                   QHolder$QSignalHolder8
                                   QHolder$QSignalHolder9
                                   QHolder$QMethod0
                                   QHolder$QMethod1
                                   QHolder$QMethod2
                                   QHolder$QMethod3
                                   QHolder$QMethod4
                                   QHolder$QMethod5
                                   QHolder$QMethod6
                                   QHolder$QMethod7
                                   QHolder$QMethod8
                                   QHolder$QMethod9)
        '(com.trolltech.qt.core Qt$ConnectionType))

(def- slot-struct (create-struct :obj :arity))

(def- qmethods 
  (vec
    (for [i (range 10)]
      (eval (symbol (str "QHolder$QMethod" i))))))

(defn make-slot [f arity]
  "Wraps f in a qt slot with a fixed arity"
  (if (> arity 9)
    (throw (Exception. "Clojure slots cannot have more than 9 args"))
    (struct slot-struct
      ; a proxy of slot-type with the 'slot' method set to f
      (proxy 
        [(nth qmethods arity)] [] 
        (method
          ([] (f))
          ([&rest] (f &rest))))
      arity)))

(def- signals 
  (vec 
    (for [i (range 10)] 
      (eval `(fn [] 
                (let [holder# ( ~(symbol (str "QHolder$QSignalHolder" i ".")) )]
                  (set! (. holder# signal) (new ~(symbol (str "QSignalEmitter$Signal" i)) holder#))))
                  ))))

(defn make-signal [arity]
  "Makes a signal of with a fixed arity. The signals arguments are all Objects so 
   this signal cannot be directly connected to a c++ slot."
  (if (> arity 9)
    (throw (Exception. "Clojure signals cannot have more than 9 args"))
    ((nth signals arity)) ))

; need exception handling in here - by default errors in signals are discarded
; could have an optional logging agent as an arg?
; want to be able to handle normal slots as well?
(defn connect [signal slot]
  "Connect a qt signal to a wrapped clojure function (made with make-slot).
   The signal and slot must have the same arity."
  (.connect signal (:obj slot)   ; note this is the connect method, not the connect function
    (str 
      "method("  
      (apply str (interpose ", " (replicate (:arity slot) "Object")))
      ")")
    (. Qt$ConnectionType QueuedConnection)))

(defn disconnect [signal slot]
  "Disconnect a qt signal from a wrapped clojure function"
  (.disconnect signal (:obj slot)   ; note this is the disconnect method, not the disconnect function
    (str 
      "method("  
      (apply str (interpose ", " (replicate (:arity slot) "Object")))
      ")")))