# 🎨 Auto-MSPaint Tool

## ⁉ What is this?
this is an automatic paint tool *(yes, it can be used in other paint programs)* made in Python

## 📦 Libraries
> **NOTE**: To easily install all the required libraries, just type in the terminal command `python -m pip install -r requirements.txt`
 - OpenCV
 - pynput
 - Pillow (PIL)

## ❓ FAQ
 - What did you use this for?
    - Bad apple
 - Can I use this on other paint programs like Adobe Photoshop and GIMP?
    - Yes.
 - How do I turn the output images into a video?
    - Using ffmpeg.

## ❓ How To Use ffmpeg to turn a video in to mspaint drawings
 **1.** First get the individual frames
   ```
   ffmpeg -i video.mp4 frames/%05d.jpg -hide_banner
   ```
 **2.** Run the Python script to automatically create the `input.txt` file.
   ```
   py make_input.py
   ```
 **3.** Render the frames by running `main.py`

 **4.** To compile everything into a video use this command
   ```
   C:\Users\Developer\FFMPEG\bin\ffmpeg.exe -f concat -i input.txt -c:v libx264 -r *FPS HERE* -pix_fmt rgb24 video/temp.mp4
   ```
 **4.5.** To add the source audio to the output video use this command after `Step 4`
   ```
   C:\Users\Developer\FFMPEG\bin\ffmpeg.exe -i video.mp4 audio.mp3
   C:\Users\Developer\FFMPEG\bin\ffmpeg.exe -i video/temp.mp4 -i audio.mp3 -map 0:v -map 1:a -c:v copy -shortest video/output.mp4
   ```