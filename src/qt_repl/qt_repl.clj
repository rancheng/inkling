; A clojure repl for interactive qt development

(in-ns 'qt-repl)
(clojure/refer 'clojure)

(import '(com.trolltech.qt.gui QApplication)
        '(java.io PushbackReader InputStreamReader PrintWriter OutputStreamWriter)
        '(java.util.concurrent SynchronousQueue))

(def app nil)
(defn init [] 
  "Start a new QApplication."
  (def app (QApplication. (make-array String 0))))

(defn- repl-on [in out]
  (let [code-box (SynchronousQueue.)
        read-agent (agent nil)]

    ; 'it' holds the last value produced by the repl
    (def it)

    (binding [it nil
              *in* in
              *out* out]

      ; the read-agent handle console interaction and sends completed strings to the main loop.
      ; exceptions are simply passed through
      (send-off read-agent 
        (fn read-loop [unused]
          (. code-box (put
            (try 
              (read *in* true nil true)
              (catch Exception e e))))
          (send-off read-agent read-loop)))

    ; main loop evals code when available, otherwise runs qt event loop
      (loop [code nil]
        (if code
          (try 
            (set! it (eval code))
            (prn it)
            (catch Exception e (do 
              (set! it e)
              (prn e))))
          (. QApplication (processEvents)))
      (recur (. code-box (poll)))))))

(defn repl
  "Start a new clojure repl which allows interactive qt development.
   The qt event loop will run in between successive evaluations."
  ([] (repl-on *in* *out*))
  ([in out] (repl-on in out)))

(defn pr-trace [exc] 
  "Print an exceptions stack trace to System.out"
  (. exc (printStackTrace (PrintWriter. *out*))))

(defn exit [] 
  "Exit the current QApplication."
  (. QApplication (exit 0)))