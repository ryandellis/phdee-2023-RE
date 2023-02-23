/*==================================================
project:       
Author:        Ryan Ellis 
E-email:       
url:           
Dependencies:  
----------------------------------------------------
Creation Date:    22 Feb 2023 - 20:57:54
Modification Date:   
Do-file version:    01
References:          
Output:             
==================================================*/

/*==================================================
              0: Program set up
==================================================*/
version 17
drop _all

import delimited "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5\instrumentalvehicles.csv"

local outputpath "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4\output"
cd "`outputpath'"
/*==================================================
              1: ivregress liml
==================================================*/


*----------1.1:
ivregress liml price car (mpg = weight), vce(robust)
estimates store liml

outreg2 using "liml.tex", tex(frag) replace label 

*----------1.2:
weakivtest





exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1.
2.
3.


Version Control:


