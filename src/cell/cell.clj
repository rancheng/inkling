(ns cell
  (:uses utils slot clojure.set))

(def- cell-struct (create-struct :valf :val :args :dependents :is-modified :is-updating :on-modified :modified-slot))

(defn add-dep [dep-cell arg-cell]
  (dosync 
    (let [{dependents :dependents :as c} @arg-cell]
      (alter arg-cell assoc :dependents (conj dependents dep-cell)))))

(defn remove-dep [dep-cell arg-cell]
  (dosync 
    (let [{dependents :dependents :as c} @arg-cell]
      (alter arg-cell assoc :dependents (disj dependents dep-cell)))))

(defmacro cell [args & valf]
  (let [cell-inner 
          (fn [args valf]
            (dosync
              (let [new-cell (ref (struct cell-struct valf (valf) args #{} false false (signal 0) nil))]
                (doseq arg args
                  (add-dep new-cell arg))
                new-cell)))]
    `(~cell-inner ~args (fn [] ~@valf))))

(defmacro defcell [name args & valf]
  `(def ~name (cell ~args ~@valf)))

; Used to delay modified signals till transaction completes
(def- modify-agent (agent nil))

(defn modified [cell]
  (dosync
    (when (not (:is-modified @cell))
      (alter cell assoc :is-modified true)
      (doseq dep (:dependents @cell) (modified dep))
      (let [om (:on-modified @cell)] 
        (send modify-agent (fn [_] (. om (emit)))))
      nil)))

(defmacro cell-set [cell & new-valf]
  (let [cell-set-inner 
          (fn [cell new-valf]
            (dosync
                (alter cell assoc :valf new-valf)
                (modified cell)))]
    `(~cell-set-inner ~cell (fn [] ~@new-valf))))

(defn cell-get [cell] 
  (dosync
    (let [{:keys [is-modified is-updating valf val] :as c} @cell]
      (when is-updating (throw (Exception. (str "Cycle found at cell:" cell))))
      (if (not is-modified)
        val
        (do
          (alter cell assoc :is-updating true)
          (let [new-val (valf)]
            (alter cell assoc :is-updating false :is-modified false :val new-val)
            new-val))))))

(defn unhook [cell]
  (dosync
    (doseq arg (:args @cell) (remove-dep cell arg))
    (doseq dep (:dependents @cell) (unhook dep))
    (disconnect (:on-modified @cell))
    ; would like to somehow disconnect slot as well
    ))

(defn modified-slot [cell] 
  (dosync
    (or (:modified-slot @cell)
        (let [ms (slot 0 #(modified cell))]
          (alter cell assoc :modified-slot ms)
          ms))))

(defn on-modified [cell] (:on-modified @cell))