(ns pen
  (:uses utils canvas cell)
  (:imports (com.trolltech.qt.gui QGraphicsPathItem QPainterPath)))

(defcell path [] nil)
(defcell path-item [path] nil)

(defn pen-down [pos]
  (dosync 
    (let [p (QPainterPath. pos)
          i (QGraphicsPathItem.)]
      (. scene (addItem i))
      (cell-set path p)
      (cell-set path-item
        (doto i (setPath (decell path)))))))

(defn pen-move [pos]
  (dosync
    (. (decell path) (lineTo pos))
    (modified path)))

(defn pen-up [pos]
  (dosync
    (cell-set path-item nil)
    (cell-set path nil)))

(def pen-tool
  {:press pen-down
   :2press pen-down
   :release pen-up
   :move pen-move})
   
(dosync (alter tools #(assoc % lbutton pen-tool)))