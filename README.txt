These tools are distributed in the hope that they will be useful - but WITHOUT
ANY WARRANTY.

I'm not the creator of the w3strings decoder (w3strings.exe), please check its readme file.

Usage:

python dual_sbutitles.py source_lang target_lang location

Example:

To have french extra subtitles for polish subtitles:
python dual_subtitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3"

Or if you want to play it safer, just on the folders that contain the locales:

python dual_subtitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\content"
python dual_subtitles.py fr pl "C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\dlc"

To know the codes for languages, look at the filenames of w3strings files, for example here:
C:\Program Files (x86)\Steam\steamapps\common\The Witcher 3\content\content0
