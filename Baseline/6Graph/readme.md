# 6Graph

This is a tool for IPv6 address pattern mining by learning the distribution of known active addresses. Its idea is introduced in the paper "6Graph: A Graph-Theoretic Approach to Address Pattern Mining for Internet-wide IPv6 Scanning".


## How to run ?


###  Convert Seeds
Please convert your IPv6 seeds to ```numpy```  binary file. We recommend the works of Gasser et al for the seeds : [IPv6 Hitlist](https://ipv6hitlist.github.io/).

For example:

    2001:12f0:700:20::67
    2001:12f0:700:f000::40
    2001:12f0:700:f000::59
To

    [
        [ 2  0  0  1  1  2 15  0  0  7  0  0  0  0  2  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  6  7]
        [ 2  0  0  1  1  2 15  0  0  7  0  0 15  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  4  0]
        [ 2  0  0  1  1  2 15  0  0  7  0  0 15  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  5  9]
    ]

Make sure the file name of seeds is __seeds__

Using:

```shell
    python convert.py
```


### Run 6Graph 

6Graph can automatically mine high-density IPv6 regions and display them.

Using:

```shell
    python main.py
```

Use those "high-quality" address regions for IPv6 scanning with your choose tools. We recommend using [Zmap](https://github.com/tumi8/zmap).




nohup /home/chengdaguo/anaconda3/envs/6Graph/bin/python /home/chengdaguo/ipv6/Baseline/6Graph/main_v3.py &

nohup /home/chengdaguo/anaconda3/envs/6Graph/bin/python /home/chengdaguo/ipv6/Baseline/6Graph/Alias_Prefix_v2.py &