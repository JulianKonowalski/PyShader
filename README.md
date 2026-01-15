# PyShader
This app allows for previewing fragment shaders in real time. The user can edit and recompile the 
shader source code during runtime.

![Program Screenshot](assets/screenshot.png)

## Cloning
To clone and run this app use:
```
git clone https://github.com/JulianKonowalski/PyShader.git
cd PyShader
pip install -r requirements.txt
python src/main.py
```

## Building
If you want to build the application you will have to do it locally. A precompiled executable cannot
be distributed due to the need of preprocessing the source code (paths to assets must match at runtime).
There's a dedicated build script in `scripts` directory. You can invoke it from anywhere you like:
```
python scripts/build.py
```
This will preprocess the source code, create a `dist` folder with a built binary and copy the needed 
assets there. As long as assets stay there, you can move the binary anywhere you like and the app should
work fine.

## Usage
The app allows you to:
* Load shaders
* Save shaders

You can use any of these actions by clicking the corresponding icon on the main task bar.