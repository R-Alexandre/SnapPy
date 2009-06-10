#!/bin/bash
# SnapPy requires Togl, a OpenGL widget for the Tk libary.  For OS X
# and Linux, binaries for Togl are provided in the snappy/ directory,
# this script is only needed if, for some reason, those fail to work.
#
# This script builds this libary in two cases:
# 
#   -Mac OS 10.5, against Tk 8.4
#   -Linux, against Tk 8.5
# 
# You should be able to modify it, or follow the steps laid out here,
# to compile Togl.  


# First, download the source if we don't have it already. Because
# Sourceforge is a little odd on how it does this, we use "wget"
# instead of "curl" or "lynx".  You may find it easier just to
# download the needed file with your webrowser..

if [ ! -e Togl2.0-src.tar.gz ]; then  
    echo "Downloading Togl2.0..."
    wget -nd http://downloads.sourceforge.net/togl/Togl2.0-src.tar.gz
fi
echo "Untaring Togl..."
tar xfz Togl2.0-src.tar.gz 
cd Togl2.0

# Set where we want Togl to be installed; this should be changed
# depending on your OS and version of Tk.  


if [ "$(uname)" = "Darwin" ] ; then  # If this is Mac OS X
    export SNAPPY_INSTALL=`pwd`/../snappy/darwin-tk8.4
else # Assume it's Linux
    export SNAPPY_INSTALL=`pwd`/../snappy/linux2-tk8.5
fi

# Now build Togl:


if [ "$(uname)" = "Darwin" ] ; then  # If this is Mac OS X

./configure --prefix=$SNAPPY_INSTALL --libdir=$SNAPPY_INSTALL
make CFLAGS='-arch ppc -arch i386' \
CPPFLAGS='-arch ppc -arch i386 \
-I/Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/Tk.framework/Versions/8.4/Headers \
-I/Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/Tk.framework/Versions/8.4/Headers/tk-private \
-I /Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/Tcl.framework/Versions/8.4/Headers \
-I /Developer/SDKs/MacOSX10.5.sdk/System/Library/Frameworks/Tcl.framework/Versions/8.4/Headers/tcl-private'

else #Presume we have Linux here:

./configure --prefix=$SNAPPY_INSTALL --libdir=$SNAPPY_INSTALL \
   --with-tcl=/usr/share/tcltk/tcl8.5/ --with-tk=/usr/share/tcltk/tk8.5/ 
make

fi 



# and finally install it:

make install-lib-binaries