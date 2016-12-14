# 脚本简介

> 作者：huanghui  
> 统计工程中未使用的png

### 特点

1. 可以搜索**xib**文件； 
2. 同时支持Android及iOS**双系统**png图片搜索；
3. 显示统计未使用图片**名称及其大小**，用于评估；
4. **单倍图**提示。因单倍图已不需要存在或者改成双倍或三倍图，需要警示；
5. **可能误搜图片提示**。某些图片写法是拼接的方式，这些图片基本都是带数字的，会被提示出来；
6. iOS**屏蔽应用icon和launch**。icon一般不会出现的代码中，所以排除它；
7. 文件命名不正确提示。比如，icon@2x-0.png;

# 使用方法

~~~
Usage: python find_unused_pics.py [optinos] image_path search_path

Options:
  -h, --help     show this help message and exit
  -a, --android  Search in Android project.(表明是搜索安卓工程)
  -d, --delete   Delete the unused pics.(表明搜索到即删除掉，慎用~)
~~~

### 详解：

~~~
python find_unused_pics.py 代表执行脚本  
image_path 表示图片文件夹，会递归搜索图片
search_path 表示需要搜索的代码文件夹

[option]
-h 查看使用参数
-a 表明是搜索安卓工程
-d 表明搜索到即删除掉，慎用~
~~~

# 注意

若提示ag命令找不到，请安装ag库。可用brew安装，命令如下：

> brew install ag
