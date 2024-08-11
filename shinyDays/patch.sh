#!/bin/bash

# Shiny Days restore script ported to bash
# While I myself have severe distaste for the content this patch restores
# I still see the value in making it easier to use on linux
# Needs xdelta3 installed to work properly
# Place it in the patch folder and run it (but read the readme below first)
# Below is the readme for the original patch script
# It applies very much here

# Shiny Days Content Restore Patch for 1.01e JAST USA Edition
# ------------------------------------------------------------

# Easy Method
# 1. Extract patch folder to Shiny Days game folder e.g. C:\SHINYDAYS\patch
# 2. Run patch.sh from inside the patch folder

# Manual Method
# 1. Extract to a temporary folder
# 2. Open Command Prompt to said temporary folder
# 3. Use the command xdelta3 -d -s <shinydayspath>\<file you are patching> <patchfile>.xdelta <a temporary folder>
# 4. Copy all patched files from the temporary folder back into the Shiny Days game folder
# 
# These patches work ONLY with Shiny Days 1.01e. Make sure you patched up the original game first before trying to use these patches or they will fail.

errorlevel=0

if [ ! -f Event04.xdelta ]; then
    errorlevel=1
fi
if [ ! -f Ex01.xdelta ]; then
    errorlevel=1
fi
if [ ! -f Movie04.xdelta ]; then
    errorlevel=1
fi
if [ ! -f MovieZ4.xdelta ]; then
    errorlevel=1
fi
if [ ! -f Script.GPK ]; then
    errorlevel=1
fi
if [ ! -f System.xdelta ]; then
    errorlevel=1
fi
if [ ! -f Voice04.xdelta ]; then
    errorlevel=1
fi
if [ ! -f RouteProcSD.xdelta ]; then
    errorlevel=1
fi
if [ ! -f SysMenuSD.xdelta ]; then
    errorlevel=1
fi
if [ ! -f ../RouteProcSD.dll ]; then
    errorlevel=1
fi
if [ ! -f ../SysMenuSD.dll ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/Event04.GPK ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/Ex01.GPK ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/Movie04.GPK ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/EventZ4.GPK ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/Script.GPK ]; then
    errorlevel=1
fi
if [ ! -f ../Packs/System.GPK ]; then
    errorlevel=1
fi

if [ $errorlevel -eq 0 ]; then
    echo "All files accounted for"
fi
if [ $errorlevel -eq 1 ]; then
    echo "One or more required files is missing. Please place the patch files in <SHINYDAYS folder>/patch"
    exit 1
fi

shinydir=$(cd .. && pwd)
patchdir="../Patched"

mv ../RouteProcSD.dll ../Packs/RouteProcSD.GPK
mv ../SysMenuSD.dll ../Packs/SysMenuSD.GPK
mkdir -p $patchdir

echo "Patching..."
for g in *.xdelta; do
    xdelta3 -d -s "../Packs/${g%.*}.GPK" "$g" "$patchdir/${g%.*}.GPK"
done

echo "Replacing files..."
cp -f Script.GPK ../Packs/Script.GPK
mv -f "$patchdir"/*.GPK ../Packs/

mv ../Packs/RouteProcSD.GPK ../RouteProcSD.dll
mv ../Packs/SysMenuSD.GPK ../SysMenuSD.dll

echo "Files patched! Enjoy your game."
exit 0
