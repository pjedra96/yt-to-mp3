import tkinter as tk
from tkinter import ttk, messagebox
import pathlib, os
import time
import yt_downloader

# global vars
current_dir = pathlib.Path(__file__).parent.resolve()
options = [("Youtube Video", 1),("Youtube Playlist", 2),("Video to MP3", 3)]
resolution = ('360p', '720p', '1080p', '2160p')

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		
		self.option_value = tk.StringVar()
		self.option_value.set(1)  # initializing the choice, i.e. Python
		self.resolution_val = '360' # default resolution
		self.progress_val = tk.IntVar()

		# configure the root window
		self.title('')
		# set up an icon
		icon = tk.PhotoImage(file=os.path.join(current_dir, 'images/youtube-downloader.png'))
		# apply the icon to the tkinter window
		self.wm_iconphoto(True, icon)

		self.geometry('500x280')
		self.configure(background='white')
		self.resizable(False, False)

		self.label = tk.Label(height=2, width=25, text='YouTube Downloader', font=('Poppins',26), fg='white', bg='#D8302F')
		self.label.place(x=0, y=0)

		# URL text box
		self.label_url = tk.Label(height=2, width=10, text='Video URL: ', font=('Poppins',10), fg='black', bg='white')
		self.label_url.place(x=0, y=90)

		self.url = tk.Text(height=1, width=50, borderwidth=1)
		self.url.place(x=90, y=100)
		#self.url.insert('1.0', 'URL of the video...')
		#self.url.bind("<FocusIn>", lambda args: self.url.delete('1.0', 'end'))

		def download():
			# if no URL entered
			if len(self.url.get("1.0", 'end')) == 1:
				messagebox.showinfo("Error", "No URL entered in the textbox")
			else:
				self.progress_val.set(40)
				self.resolution_val = self.resolution_box.get()

				if self.option_value.get() == "1" or self.option_value.get() == "2":
					# if download playlist
					if self.option_value.get() == "2":
						# get the url value
						self.link = self.url.get(1.0, 'end')
						youtube_downloader.download_playlist(self.link, self.resolution_val)

						# Set progress bar to full 
						self.progress_val.set(100)
					# if download single video
					if self.option_value.get() == "1":
						self.link = self.url.get(1.0, 'end')
						youtube_downloader.download_video(self.link, self.resolution_val)

						# Set progress bar to full 
						self.progress_val.set(100)
				# if download a video and convert to music
				elif self.option_value.get() == "3":
					self.link = self.url.get(1.0, 'end')
					filename = youtube_downloader.download_video(self.link, 'low')
					yt_downloader.convert_to_mp3(filename)
					
					# Set progress bar to full 
					self.progress_val.set(100)
				else:
					messagebox.showinfo("Error", "Invalid input!")

		def modifyGUI():
			if self.option_value.get() == "1" or self.option_value.get() == "3":
				self.label_url.config(text= "Video URL: ")
			elif self.option_value.get() == "2":
				self.label_url.config(text= "Playlist URL: ")

		def drawOptions(self):
			index=10
			# option buttons
			for option, val in options:
				tk.Radiobutton(text=option,
					bg='lightgrey',
					borderwidth=1,
					indicatoron = 0,
					width = 18,
					padx = 20,
					variable=self.option_value,
					value=val, command=modifyGUI).place(x=index, y=135)
				index = index+150
				
			# URL text box
			self.label_resolution = tk.Label(height=2, width=10, text='Resolution: ', font=('Poppins',11), fg='black', bg='white')
			self.label_resolution.place(x=10, y=165)

			#select element
			self.resolution_box = ttk.Combobox(height=2, width=45, value=resolution)
			self.resolution_box.current(0)
			self.resolution_box.place(x=120, y=173)

			#progress bar
			self.progress_bar = ttk.Progressbar(orient='horizontal', mode='determinate', length=480, variable=self.progress_val, maximum=100).place(x=10, y=210)

			# download button
			self.download = tk.Button(height=1, width=20, text='Download', font=('Poppins',14), borderwidth=1, bg='#D8302F', fg='white', command=download)
			self.download.place(x=130, y=240)

		# Draw the options
		drawOptions(self)

if __name__ == "__main__":
	app = App()
	app.mainloop()