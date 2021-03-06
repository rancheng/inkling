(ns canvas
  (:uses utils qt-repl))

(import '(com.trolltech.qt.core Qt$MouseButton Qt$MouseButtons Qt$Alignment Qt$AlignmentFlag Qt$CursorShape QRectF)
        '(com.trolltech.qt.gui QFrame QVBoxLayout QGraphicsView QGraphicsView$ViewportAnchor QGraphicsScene QPainter$RenderHint QCursor))
 
(defonce inited (init))

(def lbutton (. Qt$MouseButton LeftButton))
(def mbutton (. Qt$MouseButton MidButton))
(def rbutton (. Qt$MouseButton RightButton))

(defn- make-buttons [button]
  (let [arr (make-array Qt$MouseButton 1)]
    (aset arr 0 button)
    (Qt$MouseButtons. arr)))

(def- buttons-cache
  {lbutton (make-buttons lbutton)
   mbutton (make-buttons mbutton)
   rbutton (make-buttons rbutton)})

(def debug-tools
  {lbutton {:press   #(println "Left press" %)
            :2press  #(println "Left 2press" %)
            :move    #(println "Left move" %)
            :release #(println "Left release" %)}
   mbutton {:press   #(println "Mid press" %)
            :2press  #(println "Mid 2press" %)
            :move    #(println "Mid move" %)
            :release #(println "Mid release" %)}
   rbutton {:press   #(println "Right press" %)
            :2press  #(println "Right 2press" %)
            :move    #(println "Right move" %)
            :release #(println "Right release" %)}})
(def tools (ref debug-tools))

(defn set-tool [button tool]
  (dosync (alter tools #(assoc % button tool)))
  nil)

(def view)

(defn fire-buttons [buttons event-type pos]
  (doseq [button tool] @tools
    (if (. buttons (isSet (buttons-cache button)))
      ((tool event-type) (. view (mapToScene pos))))))

(defn fire-button [button event-type pos]
  (let [tool (@tools button)]
    (if tool
      ((tool event-type) (. view (mapToScene pos)))
      (prn "No tool for button" button))))

(def scene 
  (doto (QGraphicsScene.)))
  
(def align
    (let [arr (make-array Qt$AlignmentFlag 2)]
    (aset arr 0 (. Qt$AlignmentFlag AlignTop))
    (aset arr 1 (. Qt$AlignmentFlag AlignLeft))
    (Qt$Alignment. arr)))

(def view
  (doto
    (proxy [QGraphicsView] []
      (mousePressEvent [event] 
        (fire-button (. event (button)) :press (. event (pos))))
      (mouseReleaseEvent [event] 
        (fire-button (. event (button)) :release (. event (pos))))
      (mouseDoubleClickEvent [event] 
        (fire-button (. event (button)) :2press (. event (pos))))
      (mouseMoveEvent [event] 
        (fire-buttons (. event (buttons)) :move (. event (pos))))
      )

    (setRenderHint (. QPainter$RenderHint Antialiasing) true)
    (setScene scene)
    (setAlignment align)
    (setResizeAnchor (. QGraphicsView$ViewportAnchor NoAnchor))))

(defn cursor-off []
  (. view (setCursor (QCursor. (. Qt$CursorShape BlankCursor)))))

(defn cursor-on []
  (. view (setCursor (QCursor. (. Qt$CursorShape ArrowCursor)))))

(def layout 
  (doto (QVBoxLayout.)
    (addWidget view)))

(def frame 
  (doto (QFrame.)
    (setLayout layout)
    (show)))