# algorithm-visualizer-project
software to visualize graph coloring algorithm

# Introduction
This project is an implementation of an online algorithm called MINADM[1].
The algorithm colors the network following a few steps.


# Setup
### Dependencies
* NetworkX
* Tkinter
* PIL
```
$ pip install Networkx
$ pip install Tkinter
$ pip install Pillow
```
# Technology
* python 3.10

It is recommended to use Pycharm, you'll have to install the packages, but it is far more convenient.

# Acknowledgement
This work was done with Anya H. during our degree under the supervision of Prof. Shmuel Zaks.


# DEMO 
Welcome page

![image](https://user-images.githubusercontent.com/62480878/176378204-e2dd4d8f-1d11-4419-a01b-4be8994b252c.png)

You can choose any topology you want- path or ring topology.
After choosing you can build your own network, you can choose any size of network you want and any possible path and see the process of the coloring.

![image](https://user-images.githubusercontent.com/62480878/176379525-ae0c13af-3289-4f9c-924d-34801e901c5f.png)
![image](https://user-images.githubusercontent.com/62480878/176379629-4419a611-62bf-44e2-9b14-96f696ac213e.png)
![image](https://user-images.githubusercontent.com/62480878/176379655-64f8a3b5-37be-44d2-9f94-cef5eef37a8b.png)

Another functionality is that you can compare some network over the optimal solution and see where the online algorithm MINADM colors the paths differently.
Also, you can see the number of ADMs used using the optimal solution and the solution of the algorithm.

![image](https://user-images.githubusercontent.com/62480878/176379739-48461d78-0302-4db6-afcf-17c1163ea37a.png)

The last functionallity of the software is the ratio analysis. In the thirs tab you can do two things, either to calculate the analysis on the network the user inputs or see the 3D graph where you can see the average ratio we got after running the algorithm over different sized networks and paths.

![image](https://user-images.githubusercontent.com/62480878/176379877-a010418b-bf21-4388-951f-547a7b63a92d.png)


### ENJOY!


# References
[1] = Shalom, M., Wong, P. W., & Zaks, S. (2007, September). Optimal on-line colorings for minimizing the number of ADMs in optical networks. In International Symposium on Distributed Computing (pp. 435-449). Springer, Berlin, Heidelberg.
