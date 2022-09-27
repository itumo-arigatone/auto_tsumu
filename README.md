use python and opencv.

I want automatic play tool for tsumu-tsumu.

# Make execution environment for Win
## install python
https://www.python.org/downloads/windows/  
This repository uses python 3.9.5

## install OpenCV
1. Open cmd
2. Execute below command ↓
```
pip install opencv-python
```

## install PyAutoGui
1. Open cmd
2. Execute below command ↓
```
pip install xlib
pip install wheel
pip install pyautogui
```

## build
electron application build command
```
npm run build:render
npm run build:main
```
render is move webpack command
main is move tsc command  
```
package:windows
```

## install Vysor
https://www.vysor.io/

## How to debug auto_tsumu
```sh
npm start
```
1. Start the Vysor. And make Android controllable.
2. Enter the name of the Vysor window in the textbox.
3. Click the start button.
