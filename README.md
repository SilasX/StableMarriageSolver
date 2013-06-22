This implements a solution to a variant of the Universities/Residents Problem, itself a generalized version of the Stable Marriage Problem.

In this version, there is a many-to-one relationship between one gender and the other (specifically, requiring that the count of one be an integer multiple of the other).  The larger "gender" is called "students" here, and the smaller, "schools".

Also, the schools do not have an explicit preference ordering over students; rather, both the students and schools have qualities measured by a vector (default length 3) and the schools' preference over students is measured by the dot product of their own quality vector with that of each student, with a greater dot product preferred.  (In the solution as implemented, the universities' implicit preferences are only looked up if the students no longer uniquely determine a solution.)

MIT License
