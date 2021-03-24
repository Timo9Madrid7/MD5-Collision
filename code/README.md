## Code Structure
* cpp
    * DTU_Thomsen_MD5Col  
    *The original idea is provided by Dr. Søren Steffen Thomsen, and his website is [MD5 collision finder](http://www2.mat.dtu.dk/people/oldusers/S.Thomsen/wangmd5/). He uses C code to build the collision finder.*
        * DTU_Thomsen_MD5Col.cpp contains the source code
        * DTU_Thomsen_MD5Col.sln can be opened by Visual Studio
    * Fast_MD5Col  
    *The original idea if provided by Dr. Vlastimil Klima, and his website is [Vlastimil Klíma](https://cryptography.hyperlink.cz/).*
        * MD5Col.cpp contains the source code
        * MD5Col.sln can be opened by Visual Studio
* java
    * jar
        * MD5-Collider.jar is the java application of MD5Collision.java
    * MD5Collision.java is based on Klíma's scheme with tunnels
    * MD5Encryption.java is the forward computation of the MD5 message-digest algorithm
    * WangCol.java is based on Wang's scheme using the multi-message modification
* python
    * MD5Encryption.ipynb is the forward computation of the MD5 message-digest algorithm
