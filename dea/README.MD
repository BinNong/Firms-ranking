---
typora-root-url: ./resources
---

# 一、安装环境

#### Python安装

推荐使用conda来管理python环境，避免python版本冲突，本项目使用python3.5.6。(:warning:3.6以上版本暂不支持，因为底层的计算库不支持)。安装命令如下：

```bash
  >> conda create -n dea python=3.5.6
```

​     :cry: 如果环境安装过慢可使用，可将conda下载镜像设置成清华镜像源：

```bash
  >> conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  >> conda create -n dea python=3.5.6
```
如果没有conda，可以安装

[miniconda]: https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install



# 二、依赖安装

- #### 安装计算dea计算工具

本项目依赖数学优化工具，比如线性规划等。因此需要安装相关的依赖。依赖库在同级目录下的lib文件夹内。安装命令如下：

```bash
  >> cd lib
  >> pip install .
```

- #### 测试是否安装成功

  - [x] 第一种方法，如果是本地安装可以使用下面的命令快速验证

  ```bash
  >> pyDEA
  ```

  如果出现下图所示，表明安装成功：

  <img src="./pyDEA.png" alt="pyDEA" style="zoom:30%;" />

  - [x] 第二种方法，如果是在远程服务器安装，可使用如下方法：

    1. 进入python环境

       ```bash
       >> python
       ```
    2. 导入相关的包，如果成功即可表示安装成功
    
       ```
       >> import pyDEA.core.utils.dea_utils
       ```
    
# 三、运行

- #### 代码说明

  1. 主程序在main.py中

  2. 输入和输出数据在data目录中

- #### 代码运行

  ```bash
  >> python main.py
  ```
  
- #### 运行结果
  
  运行结果保存在data文件下，命名含有result的文件，打开之后会看如下表中的数据。
  
  如下表是保存运行结果的一张表，有两列，第一列是公司名，第二列是生产效率。

| DMU  | Efficiency |
| :--: | :--------: |
|  C1  |    1.0     |
|  C2  |    1.0     |
|  C3  |    1.0     |

:warning:输出excel文件，含有多张表单，目前只使用EfficiencyScores这张表单。