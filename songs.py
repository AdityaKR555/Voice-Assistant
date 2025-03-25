songs = "play jumme ki raat hai"

# songList = songs.split(" ")

# songList.remove('play')
# print(songList)

# song_name = ""

# for s in songList:
#     song_name = song_name + " " + s

# print(song_name)

song_name = " ".join(songs.split(" ")[1:])  # Removes "play" and joins the rest
print(song_name)