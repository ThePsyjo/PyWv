TEMPLATE = app

DEPENDPATH += . classdir
INCLUDEPATH += . classdir
OBJECTS_DIR += tmp
MOC_DIR += tmp
RCC_DIR += tmp

CONFIG += silent release

# Input
SOURCES += app.py \
           classdir/window.py \
           classdir/webWidget.py \
           classdir/plugin_nagvisWidget.py \
           classdir/genericWidget.py \
           classdir/config.py \
           classdir/linkInput.py \
           classdir/pluginHelper.py \
           classdir/trayManager.py


TRANSLATIONS += classdir/German.ts classdir/C.ts
RESOURCES += res/res.qrc
