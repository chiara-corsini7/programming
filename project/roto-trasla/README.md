# roto-trasla
<tt>roto-trasla</tt> is a python program to rotate translate and clone molecular <i>.xyz</i> files.
In the following, the basic theory of the program will be presented together with the structure of the project and a tutorial for the usage.

## Rotations

In geometry, various formalisms exist to express a rotation in three dimensions as a mathematical transformation. 
A basic rotation (also called elemental rotation) is a rotation about one of the axes of a coordinate system.
Basic rotations along the $x$, $y$ or $z$ axis in three dimensions can be represented by a 3x3 matrix, which multiplied to a vector perform the wanted rotations.
Following the right-hand rule, counter clockwise rotations by angles $\theta_x$, $\theta_y$ and $\theta_z$ are expressed along the $x$, $y$ and $z$ axes with three matrices
