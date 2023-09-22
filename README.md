![](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/School_Days_Logo.svg/250px-School_Days_Logo.svg.png)  
Scripts created for School Days HQ modding, can't guarantee perfect compatibility with Shiny Days

# Getting Started
Before you begin modding this game you need to extract all of the files from the GPKs. You can do this with [Crage](http://ucla.jamesyxu.com/?p=50), and by using the following command.
```
crage.exe -d "E:\Games\School Days\Packs" -O exe="E:\Games\School Days\SCHOOLDAYS HQ.exe" 
```
Make sure to replace the directorys with where you installed the game, or else it won't work. After this copy the outputted files into the games directory, then rename /Packs/ to something like /.Packs/ so it doesn't load from there anymore. Then you are free to edit the games scripts and replace any files you want, just make sure that:

Movie files are encoded in WMV  
Audio files are encoded in Vorbis OGG  
Image files are encoded in PNG

Movie and image files by default won't scale correctly to the screen if they are bigger then the original size, I've found setting [UseYUVSetting] inside of /Ini/DX9GRAPHIC.INI to "1" can improve this, but I recommend just scaling your videos and images to fit within the original files resoluton. 
