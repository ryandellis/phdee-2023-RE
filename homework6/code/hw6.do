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
clear all
set more off

import delimited "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5\instrumentalvehicles.csv"

local outputpath "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework6\output"
cd "`outputpath'"
/*==================================================
              1: rdrobust
==================================================*/


*----------1.1:
rdplot mpg length, c(225) p(2) bwselect(mserd) genvars


rename rdplot_hat_y mpg_hat
cd `outputpath'
gr export rd_stata.png
*----------1.2:

regress price mpg_hat car, vce(robust)



exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1.
2.
3.


Version Control:


