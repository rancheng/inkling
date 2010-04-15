(ns knife
  (:uses utils canvas cell slot)
  (:imports (com.trolltech.qt.gui QGraphicsPathItem QPainterPath QGraphicsItem QPen QBrush QColor)
            (com.trolltech.qt.core  Qt$ItemSelectionMode)))

(defn knife-down [path pathitem pos]
  (dosync 
    (let [p (QPainterPath. pos)
          i (QGraphicsPathItem.)]
      (. scene (addItem i))
      (doto i 
        (setPath p)
        (setBrush (QBrush. (QColor. 255 0 0 25)))
        (setPen (QPen. (QColor. 255 0 0 50))))
      (ref-set path p)
      (ref-set pathitem i))))

(defn knife-move [path pathitem pos]
  (dosync
    (. @path (lineTo pos))
    (. @pathitem (setPath @path))))

(defn knife-up [path pathitem pos]
  (. scene (setSelectionArea (. @pathitem (path))))
  (doseq item (. scene (selectedItems))
    (. scene (removeItem item)))
  (. scene (removeItem @pathitem))
  (. scene (clearSelection)))

(defn knife-tool []
  (let [path (ref nil)
        pathitem (ref nil)]
    {:press #(knife-down path pathitem %)
    :2press #(knife-down path pathitem %)
    :release #(knife-up path pathitem %)
    :move #(knife-move path pathitem %)}))

(defn set-knife []
  (set-tool lbutton (knife-tool)))