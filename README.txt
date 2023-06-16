Usage:

python dual_sbutitles.py source_lang target_lang location

Example:
To have french extra subtitles for polish subtitles:
python dual_sbutitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3"

Or if you want to play it safer, just on the folders that contain the locales:

python dual_sbutitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\content"
python dual_sbutitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\dlc"

To know the code for languages, look at the filenames of w3strings files, for example here:
C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\content\content0