# 6hit

## 环境要求
- 安装zmap
  
    ### zmapv6 installation (ask in IPv4 network)
    
    ####  Building from Source
    
    ```
    git clone https://github.com/tumi8/zmap.git
    cd zmap
    ```
    #### Installing ZMap Dependencies
    
    On Debian-based systems (including Ubuntu):
    ```
    sudo apt-get install build-essential cmake libgmp3-dev gengetopt libpcap-dev flex byacc libjson-c-dev pkg-config libunistring-dev
    ```
    
    On RHEL- and Fedora-based systems (including CentOS):
    ```
    sudo yum install cmake gmp-devel gengetopt libpcap-devel flex byacc json-c-devel libunistring-devel
    ```
    
    On macOS systems (using Homebrew):
    ```
    brew install pkg-config cmake gmp gengetopt json-c byacc libdnet libunistring
    ```
    
    #### Building and Installing ZMap
    
    ```
    cmake .
    make -j4
    sudo make install
    ```

- 安装<text style="color: red">**Python3**</text>依赖包
~~~bash
pip3 install iteration_utilities
~~~

- 其他注意事项
    - 确认存在zmap文件夹（保存scan的中间结果）
    - 如果是非root用户运行，需要修改term的密码过期时间为0或-1，即直到下一次打开终端或者永不过期
    
## 运行
- 参数
    - 参数修改在main.py的 super params 部分，含义见注释
- 运行
~~~bash
# 清空上一次的记录
bash run.sh
~~~
或者
~~~bash
# 保存上一次的记录
sudo zmap
python3 main.py
~~~
- 结果
    - 每次运行的结果目前没有保存，只有探测数量随轮次的记录保存在progress.txt中
    - 如果需要处理结果输出图像，可以调用progress.py程序，可能得根据需要修改str2timestamp函数