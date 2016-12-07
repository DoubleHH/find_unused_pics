# 脚本简介

> 作者：huanghui  
> 统计工程中未使用的png。目前xib所使用的图片搜不到

# 使用方法

~~~
python find_unused_pics.py image_path project_source_path del(option)
~~~

### 详解：

~~~
python find_unused_pics.py 代表执行脚本  
image_path 表示图片文件夹，会递归搜索图片
project_source_path 表示代码文件夹
del 是可选参数，若写了标示将未用图片删除
~~~

# 注意

若提示ag命令找不到，请安装ag库。可用brew安装，命令如下：

> brew install ag