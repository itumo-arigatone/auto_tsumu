use python and opencv.

I want automatic play tool for tsumu-tsumu.

# Make execution environment for Win
## install python
https://www.python.org/downloads/windows/

## install OpenCV
1. Open cmd
2. Execute below command ↓
```sh
pip install opencv-python
```

## install PyAutoGui
1. Open cmd
2. Execute below command ↓
```sh
pip install xlib
pip install wheel
pip install pyautogui
```

## build
electron application build command
```sh
npm run build:render
npm run build:main
```
render is move webpack command
main is move tsc command

## install Vysor
https://www.vysor.io/

## use auto_tsum
```sh
npm start
```
1. enter the name of the window in the textbox.
2. click the start button.
