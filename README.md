# two-stage-robust-MG



复现中国电机工程学报《微电网两阶段鲁棒优化经济调度方法》

根据文中的强对偶理论编程求解时出现了一些问题，因此重新推导了模型的KKT条件进行求解

语言：Python 3.10.1 + Gurobi 10.0.1

程序说明：twostageMG.py为非紧凑形式的约束，KKTmatrix.py将非紧凑形式的约束转化为紧凑形式，MGCCGKKT为采用KKT方法的CCG两阶段鲁棒求解程序，运行MGCCGKKT.py即可，如果想采用benders分解可以运行benders_decomposition.py

![image](https://user-images.githubusercontent.com/51228607/236673307-288f25e8-2246-4d31-9e98-94644049e99a.png)

迭代过程

![image](https://user-images.githubusercontent.com/51228607/236673322-8d046f48-9a15-41f4-83b3-4149cf14e124.png)

光伏出力

