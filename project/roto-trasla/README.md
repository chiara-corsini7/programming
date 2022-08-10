# roto-trasla
<tt>roto-trasla</tt> is a python program to rotate translate and clone molecular <i>.xyz</i> files. In the following, the basic theory of the program will be presented together with the structure of the project and a tutorial for the usage.

## Rotations

A rotation in three dimensions can be expressed through several formalisms as a mathematical transformation. A basic rotation is a rotation about one of the axes of a coordinate system. Basic rotations along the $x$, $y$ or $z$ axis of the Cartesian coordinate systems can be represented by a 3 x 3 matrix, which multiplied to a vector perform the wanted rotations. Following the right-hand rule, counter clockwise rotations are expressed along the $x$, $y$ and $z$ axes with three matrices

<p  align="center">
 <img src="./images/rot-mat.png" width="80%" height="80%">
</p>


with $\pmb{\hat{x}},\pmb{\hat{y}},\pmb{\hat{z}}$ being the axes of the rotation and $\theta_{x},\theta_{y},\theta_{z}$ the angles of rotation in the different directions.
Other rotation matrices can be obtained from these three using matrix multiplication. For example, the product



The order of rotation operations is from right to left; the matrix adjacent to the column vector is the first to be applied, in this case along $\pmb{\hat{z}}$, and then the others. In general matrix multiplication is not commutative therefore attention must be paid when trying to invert rotations.
The rotated coordinates are obtained via matrix multiplication

<p  align="center">
 <img src="./images/ruota.png" width="30%" height="30%">
</p>

where $\pmb{v_i}$ is the vector of the coordinates of the $i^{th}$ atom and $N$ is the number of atoms.
In this general case the axis of rotation for each matrix lies on the fixed axis that lies along the respective unit vector $\pmb{\hat{n}}$. In many cases the molecules are not found in the center of the system, meaning that a general rotation along $\pmb{\hat{x}},\pmb{\hat{y}}$ and $\pmb{\hat{z}}$ also causes a displacement of the molecule inside the cell. To rotate free molecules it is necessary to define the axis of rotation of each molecule and perform the rotationa along that axis. This process requires a thorough analysis of the molecular geometry and it is hard to generalize. Therefore, it is possible to perform a fictitious rotation along the central axis of the molecule just by generally rotating the molecule along the $x$, $y$ and $z$ axes of the system and then relocating it in its original position by

<p  align="center">
 <img src="./images/ruota-rip.png" width="40%" height="40%">
</p>

where $x_{i_{rep}}$, $x_{i_{rot}}$ and $x_{i}$ are the new, rotated and original $x$ coordinate of the $i^{th}$ atom, respectively. The same also applies to the $y$ and $z$ coordinates.




## Translations

To perform translations the process is straightforward. The translated coordinates can be found by simply adding the wanted amount to the preexisting coordinates

<p  align="center">
 <img src="./images/trasla.png" width="25%" height="25%">
</p>

where $x_{i_{tra}}$ and $x_{i}$ are the new and original $x$ coordinate of the $i^{th}$ atom, respectively.and $N$ is the number of atoms. The same also applies to the $y$ and $z$ coordinates.

## Cloning and Supercell

The system can be easily cloned or replicated along each direction by defining a supercell. This is very useful in system containing bulks or surfaces, whose crystal structure can be described by means of a unit cell. The unit cell is a repeating unit formed by the vectors spanning the points of a lattice. For the same system multiple unit cells can be defined and a larger system can be obtained just by replicating the unit cell for the wanted amount.
Any three-dimensional supercell can be defined via three cell vectors $a$, $b$ and $c$ and three cell angles $\alpha$, $\beta$ and $\gamma$. Via different values of cell vectors and angles all conventional primitive cells can be derived





The supercell can be represented in matrix form

<p  align="center">
 <img src="./images/supercell.png" width="18%" height="18%">
</p>



where $(c_{11}, c_{12}, c_{13})$, $(c_{21}, c_{22}, c_{23})$ and $(c_{31}, c_{32}, c_{33})$ are the $x$, $y$ and $z$ components of the cell. From here, the cloning values can be constructed 

<p  align="center">
 <img src="./images/replica-values.png" width="60%" height="60%">
</p>

where $n_{clon_{x}}, n_{clon_{y}}, n_{clon_{z}}$ are the cloning factors in the $x$, $y$ and $z$ directions. Then the atomic coordinates can be replicated to clone the entire system

<p  align="center">
 <img src="./images/replica.png" width="30%" height="30%">
</p>

where $x_{i_{rep}}$ and $x_{i}$ are the new and original $x$  coordinate of the $i^{th}$ atom, respectively and N is the number of atoms. 


## Structure of the project

To 

