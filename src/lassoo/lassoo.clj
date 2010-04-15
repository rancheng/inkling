(ns lassoo
  (:uses utils canvas cell slot)
  (:imports (com.trolltech.qt.gui QGraphicsPathItem QPainterPath QGraphicsItem QPen QBrush QColor)
            (com.trolltech.qt.core  Qt$ItemSelectionMode QPointF)))

(defn lassoo-down [drag-info path pathitem pos]
  (dosync
    (if (some #(.. % (boundingRect) (contains pos)) (. scene (selectedItems)))

      ; Begin dragging
      (ref-set drag-info 
        {:pos pos
        :items (. scene (selectedItems))})

      ; Start a new lassoo path
      (let [p (QPainterPath. pos)
            i (QGraphicsPathItem.)]
        (. scene (addItem i))
        (doto i 
          (setPath p)
          (setBrush (QBrush. (QColor. 0 0 255 25)))
          (setPen (QPen. (QColor. 0 0 255 50))))
        (ref-set path p)
        (ref-set pathitem i))))) 


(defn lassoo-move [drag-info path pathitem pos]
  (dosync
    (if @drag-info

      ; Drag items
      (let [deltax (- (.x pos) (.x (:pos @drag-info)))
            deltay (- (.y pos) (.y (:pos @drag-info)))]
        (doseq item (:items @drag-info)
          (. item (moveBy deltax deltay)))
        (alter drag-info assoc :pos pos))

      ; Extend lassoo path
      (do
        (. @path (lineTo pos))
        (. @pathitem (setPath @path))))))

(defn lassoo-up [drag-info path pathitem pos]
  (dosync
    (if @drag-info
      ; Turn dragging off again
      (ref-set drag-info nil)
    
      ; Set selection
      (do
        (. scene (setSelectionArea (. @pathitem (path))))
        (. scene (removeItem @pathitem))))))

(defn lassoo-tool []
  (let [drag-info (ref nil)
        path (ref nil)
        pathitem (ref nil)]
    {:press #(lassoo-down drag-info path pathitem %)
    :2press #(lassoo-down drag-info path pathitem %)
    :release #(lassoo-up drag-info path pathitem %)
    :move #(lassoo-move drag-info path pathitem %)}))

(defn set-lassoo []
  (set-tool lbutton (lassoo-tool)))