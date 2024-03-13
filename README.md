# 如何将python项目打包成可执行程序
- 首先确保每一个.py文件的目录下都有__init__.py，这是帮助有助于Python识别这些目录应被视为Python包。
- 其次关闭所有杀毒软件
- 可以在pycharm的terminal中，切换到主函数所在的python文件的目录下
- 执行： 
- ```cpp
   pyinstaller --onefile --windowed xxxx.py
  ```
- 程序有修改，如果你希望每次构建都清理之前的构建结果，可以加上--clean选项，这样PyInstaller会先清除之前的构建缓存。
- ```cpp
  pyinstaller --onefile --windowed --clean xxxx.py
  ```
  
