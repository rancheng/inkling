module NoteWindow where

import Graphics.UI.Gtk.General.Structs(Rectangle)
import Graphics.UI.Gtk.Gdk.Region -- for rect intersect
import Graphics.Rendering.Cairo
import Graphics.UI.Gtk
import Data.IORef

-- Everything in here relies on nothing happening whilst drawing a stroke.
-- This is *probably* a safe assumption. We'll see how it goes.

-- Utility functions
data Pt = Pt Double Double

unPt f (Pt x y) = f x y

getX (Pt x _) = x
getY (Pt _ y) = y 

inside (x,y) (Rectangle bx by bw bh) = 
	(floor x - bx <= bw) && (floor y - by <= bh)

intersects (Rectangle ax ay aw ah) (Rectangle bx by bw bh) = 
	not (
		(bx + bw < ax) ||
		(ax + aw < bx) ||
		(by + bh < ay) ||
		(ay + ah < by)
	)

moveToP = unPt moveTo
lineToP = unPt lineTo

-- Bunch of points and their bounding box
data Stroke = Stroke [Pt] Rectangle

getRect (Stroke _ rect) = rect

-- A notewindow consists of a draw area, some completed strokes and a stroke in progress
data NoteWindow = NW DrawingArea (IORef [Stroke]) (IORef [Pt])

makeNoteWindow drawArea = do
	-- Make the note window
	r1 <- newIORef []
	r2 <- newIORef []
	let nw = NW drawArea r1 r2

	-- Hook the note window into the drawing area
	onExposeRect drawArea $ drawNW nw
	
	onMotionNotify drawArea True $ \ (Motion _ _ x y _ _ _ _) -> do
		addPt nw (Pt x y)
		return True
	--widgetAddEvents dr [ButtonMotionMask]
	widgetAddEvents drawArea [Button2MotionMask]
	widgetDelEvents drawArea [PointerMotionMask]

	onButtonRelease drawArea $ \ (Button _ _ _ x y _ _ _ _) -> do
		finishStroke nw
		return True
	
	-- on exit needed as well !!!
	
	return nw
	

--disassoc

addPt (NW da _ ptsRef) newPt = do
	pts <- readIORef ptsRef
	case pts of
		[] 	-> writeIORef ptsRef [newPt]
		(p:ps) 	-> do
			writeIORef ptsRef (newPt:p:ps)
			dw <- widgetGetDrawWindow da
			renderWithDrawable dw $ do
				moveToP p
				lineToP newPt
				stroke

finishStroke (NW _ strokesRef ptsRef) = do
	strokes <- readIORef strokesRef
	pts	<- readIORef ptsRef
	case pts of	
		[] 	-> writeIORef strokesRef strokes	
		pts	-> writeIORef strokesRef ( (Stroke pts (bounds pts)) : strokes)
	writeIORef ptsRef []

bounds pts = 
	let 	xleft   = floor   $ minimum $ map (getX) pts
		xright  = ceiling $ maximum $ map (getX) pts
		ybottom = floor   $ minimum $ map (getY) pts
		ytop    = ceiling $ maximum $ map (getY) pts
	in Rectangle xleft ybottom (xright - xleft) (ytop - ybottom)

drawStroke (Stroke [] _) = return ()
drawStroke (Stroke (p:ps) _) = do
	moveToP p
	sequence_ $ map lineToP ps
	stroke 

drawStrokes strokes rect =
	sequence_ $ map drawStroke $ filter (intersects rect . getRect) strokes
	
drawNW (NW da strokeRef _) rect = do
	strokes <- readIORef strokeRef
	dw <- widgetGetDrawWindow da
	renderWithDrawable dw $ drawStrokes strokes rect
		