# Synology Photos albums import
Synology Photos albums import from Google Takeout

Script is not ideal byt I dont find any solution to create my albums from Google Takeout in Synology Photos

Script works with normal user from Synology (no admin permission is required).

Workd witch DSM 7.

As in official doc of import photos from Google Photos using Google Takeout (https://kb.synology.com/vi-vn/DSM/tutorial/How_do_I_migrate_photos_from_Google_Photos) use <b>takeout-helper.exe</b>

After use of takeout-helper.exe you can use this script on created folder (REMAPPED_FOLDER).

Remove ALL_PHOTOS folder if you dont want album with all photo in you Synology Photos

Script creates albums from Synology Photos -> Shared Space. If you want use Personal Space then you need to change SYNO.FotoTeam... to SYNO.Foto... in code

> [!IMPORTANT]
> Copy files from REMAPPED_FOLDER\ALL_PHOTOS to you DSM folder /photo/Google_Photo_Takeout
> 
> Create at least one folder with photo from Synology Photos web interface before run script
# How it works:

- Script scan REMAPPED_FOLDER and subfolders for photos (works also witch symlinks)
- Script scan Synology Photos -> Shared Space for file using API
- Script create album or find existing album. Album name is subfolder name of REMAPPED_FOLDER. Files in subfolders year, month are appended to one album. 
- Script links files from Synology Photos to album

# Example

In REMAPPED_FOLDER you have files

> C:\Google_Photo_Takeout\My_Album\2022\12\IMG_20220109_110157865-COLLAGE.jpg
> C:\Google_Photo_Takeout\My_Album\2022\11\IMG_20220109_110157865.jpg

In Synology File Station you have files:

> /photo/Google_Photo_Takeout/2022/12/IMG_20220109_110157865-COLLAGE.jpg
> /photo/Google_Photo_Takeout/2022/11/IMG_20220109_110157865.jpg

After script you should have album <b>My_Album</b> in <b>Synology Photos -> Shared Space</b> witch files <b>IMG_20220109_110157865-COLLAGE.jpg</b> and <b>IMG_20220109_110157865.jpg</b>
   
