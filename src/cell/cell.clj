(ns cell
  (:uses utils clojure.set))

(def- cell-struct (create-struct :valf :val :args :dependents))

(defn add-dep [dep-cell arg-cell]
  (dosync 
    (let [{dependents :dependents :as c} @arg-cell
          new-arg-cell (assoc c :dependents (conj dependents dep-cell))]
      (ref-set arg-cell new-arg-cell)))) 

(defn remove-dep [dep-cell arg-cell]
  (dosync 
    (let [{dependents :dependents :as c} @arg-cell
          new-arg-cell (assoc c :dependents (disj dependents dep-cell))]
      (ref-set arg-cell new-arg-cell)))) 

(defmacro cell [args & valf]
  (let [cell-inner 
          (fn [args valf]
            (dosync
              (let [val (valf)
                    new-cell (ref (struct cell-struct valf val args #{}))]
                (doseq arg args
                  (add-dep new-cell arg))
                new-cell)))]
    `(~cell-inner ~args (fn [] (do ~@valf)))))

(defmacro defcell [name args & valf]
  `(def ~name (cell ~args ~@valf)))

(defn update [cell]
  (dosync
    (let [{:keys [valf val dependents] :as c} @cell
          new-val (valf) ;do we really want to calculate this in-sync
          new-cell (assoc c :val new-val)]
      (ref-set cell new-cell)
      (if (not= val new-val) (doseq dep dependents (update dep))))))

(defn modified [cell]
  (let [{dependents :dependents} @cell]
  (dosync (doseq dep dependents (update dep)))))

(defn decell [cell] (:val @cell)) 

(defmacro cell-set [cell & new-valf]
  (let [cell-set-inner 
          (fn [cell new-valf]
            (dosync
                (ref-set cell (assoc @cell :valf new-valf))
                (update cell)))]
    `(~cell-set-inner ~cell (fn [] ~@new-valf)))) 