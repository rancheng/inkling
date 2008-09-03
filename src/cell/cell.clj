(in-ns 'cell)
(clojure/refer 'clojure)

(load-file "/home/jamie/inkling/src/utils.clj") (refer 'utils)
(load-file "/home/jamie/clojure/src/clj/clojure/set/set.clj") (refer 'clojure.set)

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

(defmacro cell [args valf]
  (let [cell-inner 
          (fn [args valf]
            (dosync
              (let [val (valf)
                    new-cell (ref (struct cell-struct valf val args #{}))]
                (doseq arg args
                  (add-dep new-cell arg))
                new-cell)))]
    `(~cell-inner ~args (fn [] ~valf))))

(defmacro defcell [name args valf]
  `(def ~name (cell ~args ~valf)))

(defn update [cell]
  (dosync
    (let [{:keys [valf val dependents] :as c} @cell
          new-val (valf) ;do we really want to calculate this in-sync
          new-cell (assoc c :val new-val)]
      (ref-set cell new-cell)
      (if (not= val new-val) (doseq dep dependents (update dep))))))

(defn decell [cell] (:val @cell)) 

(defmacro cell-set [cell new-args new-valf]
  (let [cell-set-inner 
          (fn [cell new-args new-valf]
            (dosync
              (let [{:keys [valf val-agent args dependents]} @cell
                    new-cell (struct cell-struct new-valf val args dependents)]
                (doseq arg args (remove-dep cell arg))
                (doseq arg new-args (add-dep cell arg))
                (ref-set cell new-cell)
                (update cell))))]
    `(~cell-set-inner ~cell ~new-args (fn [] ~new-valf)))) 