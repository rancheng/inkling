module Main where

import Graphics.UI.Gtk
import Graphics.UI.Gtk.Glade
import NoteWindow


main = do
-- 	initGUI
	unsafeInitGUIForThreadedRTS
	Just xml	<- xmlNew "notes.glade"
	window		<- xmlGetWidget xml castToWindow "window1"
	da		<- xmlGetWidget xml castToDrawingArea "drawingarea1"
	onDestroy window mainQuit

	makeNoteWindow da

	widgetShowAll window

	mainGUI
