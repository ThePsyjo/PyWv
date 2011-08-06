TEMPLATE = app

DEPENDPATH += . classdir
INCLUDEPATH += . classdir
OBJECTS_DIR += tmp
MOC_DIR += tmp
RCC_DIR += tmp

CONFIG += silent release

# Input
SOURCES += app.py \
	classdir/config.py \
	classdir/genericWidget.py \
	classdir/linkInput.py \
	classdir/plugin_delayNagvisWidget.py \
	classdir/plugin_delayWidget.py \
	classdir/pluginHelper.py \
	classdir/plugin_min1024bWidget.py \
	classdir/plugin_nagvisWidget.py \
	classdir/trayManager.py \
	classdir/webWidget.py \
	classdir/window.py


TRANSLATIONS += classdir/German.ts classdir/C.ts
RESOURCES += res/res.qrc
