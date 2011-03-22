import Graphics.UI.Gtk.General.Structs(Point,Rectangle)
import Graphics.Rendering.Cairo
import Graphics.UI.Gtk

-- Utility functions
getX (x,_) = x
getY (_,y) = y 

inside (Point x y) (Rectangle bx by bw bh) = 
	(x - bx < bw) && (y - by < bh)

intersects a@(Rectangle ax ay aw ah) b@(Rectangle bx by bw bh) = 
	(inside (ax,ay) b) || (inside (bx,by) a) 

-- Bunch of points and their bounding box
data Stroke = Stroke [Point] Rectangle

getRect (Stroke _ rect) = rect

-- A notewindow consists of a draw window, some completed strokes and a stroke in progress
data NoteWindow = NW DrawWindow (IORef [Stroke]) (IORef [Points])

assoc

disassoc

addPoint dw (W _ ptsRef) newPt = do
	pts <- readIORef ptsRef
	case pts of
		[] 	-> writeIORef ptsRef [newPt]
		(p:ps) 	-> do
			writeIORef ptsRef (newPt:p:ps)
			renderWithDrawable dw $ do
				moveTo p
				lineTo p
				stroke

finishStroke (W strokesRef ptsRef) = do
	strokes <- readIORef strokesRef
	pts	<- readIORef ptsRef
	writeIORef strokesRef ( (Stroke pts (bounds pts)) : strokes)
	writeIORef ptsRef []

bounds pts = 
	let 	xleft   = minimum . map (getX) pts
		xright  = maximum . map (getX) pts
		ybottom = minimum . map (getY) pts
		ytop    = maximum , map (getY) pts
	in Rectangle xleft ybottom (xright - xleft) (ytop - ybottom)

drawStroke (Stroke [] _) = return ()
drawStroke (Stroke (p:ps) _) = do
	moveTo p
	sequence $ map lineTo ps
	stroke 

drawStrokes strokes maybeRect =
	let targets =
		case maybeRect of
			Just rect -> filter (intersects rect . getRect) strokes
			Nothing   -> strokes
	in sequence $ map drawStroke strokes