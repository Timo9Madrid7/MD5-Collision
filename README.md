# MD5_Collision
Reproduce Marc Stevens's Fastcoll algorithm based on Python
IN4253ETHackLab


Goals:

– reproduce paper

– perform a risk analysis of a real system in place

– test the security of a system and understand vulnerabilities

– develop and suggest countermeasures

- Algorithm:


![捕获1](https://user-images.githubusercontent.com/79078851/113065645-7f8f3100-91b9-11eb-84e0-244745fa0f0e.PNG)

![捕获2](https://user-images.githubusercontent.com/79078851/113065647-80c05e00-91b9-11eb-8a80-de0111cd366c.PNG)

Reference: Marc Stevens Fast Collision Attack on MD5, 2006, https://www.win.tue.nl/hashclash/fastcoll.pdf

- Optimized sufficient conditions:

![捕获3](https://user-images.githubusercontent.com/79078851/113065894-e7de1280-91b9-11eb-9c2b-b49cf9150390.PNG)

![捕获4](https://user-images.githubusercontent.com/79078851/113065895-e876a900-91b9-11eb-87bd-e0ed98af533a.PNG)

![捕获5](https://user-images.githubusercontent.com/79078851/113065896-e876a900-91b9-11eb-989f-2a07c3f54c56.PNG)

![捕获6](https://user-images.githubusercontent.com/79078851/113065898-e90f3f80-91b9-11eb-861a-e7dd16de89bb.PNG)

![捕获](https://user-images.githubusercontent.com/79078851/113065950-f9271f00-91b9-11eb-9b82-4d3d1d03f0ef.PNG)

Reference: Marc Stevens Fast Collision Attack on MD5, 2006, https://www.win.tue.nl/hashclash/fastcoll.pdf

- First, this algorithm is based on 'optimized' sufficient conditions, which is addressed in appendix A of Marc Stevens Fast Collision Attack on MD5, here more restrictions on T are applied, then algorithms applied in this project are different from Marc Steven's latest version of fast-coll, for his latest fast-coll algorithm, Tunnels were applied,  which improved performance greatly, also, Marc improved his algorithm by making changes on step 3 and 5 to improve the performance, most importantly by adding restrictions on T  for both blocks, this algorithm guarantee a collision if all 'optimized' sufficient conditions are fulfilled for both blocks.

- To end up by pointing out several issues we tackled with when implementing this algorithm with Python, first of all, as Python store data different with Java and C++ which is  widely used by this algorithm, we need to add overflow with python, which means if any number is above this limitation, it shall returned back with overflow control. Also it is  even harder for handling with transforms between different bases of data, as Python hold different bin and hex number for negative numbers compared with Java and C++.

