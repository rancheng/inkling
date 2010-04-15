(ns pen
  (:uses utils canvas cell slot)
  (:imports (com.trolltech.qt.gui QGraphicsPathItem QPainterPath QGraphicsItem QGraphicsItem$GraphicsItemFlag QGraphicsItem$CacheMode)
            (com.trolltech.qt.core QSize)))

(defn pen-down [path pathitem pos]
  (dosync 
    (let [p (QPainterPath. pos)
          i (QGraphicsPathItem.)]
      (. scene (addItem i))
      (doto i 
        (setPath p)
        (setFlag (. QGraphicsItem$GraphicsItemFlag ItemIsSelectable) true)
;       (setCacheMode (. QGraphicsItem$CacheMode DeviceCoordinateCache) (QSize. 0 0)) ; QSize isnt used - supposed to be an optional arg
        ) 
      (ref-set path p)
      (ref-set pathitem i))))

(defn pen-move [path pathitem pos]
  (dosync
    (. @path (lineTo pos))
    (. @pathitem (setPath @path))))

(defn pen-up [path pathitem pos])

(defn pen-tool []
  (let [path (ref nil)
        pathitem (ref nil)]
    {:press #(pen-down path pathitem %)
    :2press #(pen-down path pathitem %)
    :release #(pen-up path pathitem %)
    :move #(pen-move path pathitem %)}))

(defn set-pen []
  (set-tool lbutton (pen-tool)))