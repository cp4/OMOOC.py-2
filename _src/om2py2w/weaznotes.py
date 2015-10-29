#-*- encoding: utf-8 -*-

import time
import Tkinter as tk 
import ttk
import easynote.eznote as eznt 

class MyEzNote:
	def __init__(self):
		self.TextVisibleToggle = False
		self.root = tk.Tk()
		self.root.title(u"速录速查")

		self.frame = ttk.Frame(self.root, padding = "3 12 3 12")
		self.frame.grid(column = 0, row = 0)

		self.newLabelText = tk.StringVar()
		self.newLabel = ttk.Label(self.frame, text = u"新增:", padding = "3 2 3 2")#newLabelText)
		self.newLabel.grid(column = 0, row = 0)

		self.currentNote = tk.StringVar()
		self.inputBar = tk.Entry(self.frame, textvariable = self.currentNote, state = "normal", justify = "left", width = 100, disabledbackground = "#ffba80")
		self.inputBar.grid(column = 1, row = 0, columnspan = 3)
		self.inputBar.bind('<Return>', self.commitInput)
		self.inputBar.focus_set()

		#self.confirmButton = ttk.Button(self.frame, text = u"录入", width = 4, command = self.commitInput, padding = "3, 2, 3, 2")
		#self.confirmButton.grid(column = 4, row = 0)

		self.historyToggleName = tk.StringVar()
		self.historyToggleName.set(u"显示/折叠全部")
		self.historyButton =  ttk.Button(self.frame, text = u"显示/折叠全部", width = 12, padding = "3, 2, 3, 2", command = self.switchHistoryBoard)
		self.historyButton.grid(column = 5, row = 0)

		self.historyBoard = tk.Text(self.frame, width = 100, background = "#f8f8f8", foreground = "#ffba80")
		self.historyBoard.grid(column = 1, row = 1)
		self.historyBoard.grid_remove()


	def showHistory(self):
		self.historyBoard.delete("0.0","end")
		ln = 0
		for l in eznt.readnotes():
			ln += 1
			lnStr = str(ln) + '.0'
			self.historyBoard.insert(lnStr, l)
		self.historyBoard.see(lnStr)	

	def commitInput(self, event):
		eznt.recthis(self.currentNote.get())
		self.inputBar.config(state = "disabled") #change the entry bg color to assure user's input has been recorded.
		self.root.update()
		time.sleep(0.2)
		self.showHistory()
		self.inputBar.config(state = "normal")
		self.currentNote.set("")

	def switchHistoryBoard(self):
		if self.TextVisibleToggle:
			self.historyBoard.grid_remove()
			self.TextVisibleToggle = False
		else:
			self.showHistory()
			self.historyBoard.grid()
			self.TextVisibleToggle = True

	def run(self):
		self.root.mainloop()



if __name__ == '__main__':
	myeznote = MyEzNote()
	myeznote.run()

