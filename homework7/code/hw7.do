/*==================================================
project:       
Author:        Ryan Ellis 
E-email:       
url:           
Dependencies:  
----------------------------------------------------
Creation Date:     6 Mar 2023 - 20:40:31
Modification Date:   
Do-file version:    01
References:          
Output:             
==================================================*/

/*==================================================
              0: Program set up
==================================================*/
version 17
clear all

use "C:\Users/`c(username)'\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework7\data\electric_matching.dta"
/*==================================================
              1: 
==================================================*/

gen logmw = ln(mw)
format date %d
gen treat=0
replace treat = 1 if date >= td(01mar2020)

gen zon = .
replace zon = 0 if zone == "COMED"
replace zon = 1 if zone == "AE"


reg logmw treat i.zon i.month i.dow i.hour pcp temp

*----------1.1:
reg logmw treat i.zon i.month i.dow i.hour pcp temp, vce(robust)

*----------1.2:
teffects nnmatch (logmw pcp temp) (treat) if month>2, ematch(zon dow hour month)

*----------1.3:


/*==================================================
              2: 
==================================================*/


*----------2.1:
reg logmw treat i.zon i.year i.month i.dow i.hour pcp temp, vce(robust)


*----------2.2:


*----------2.3:


/*==================================================
              3: 
==================================================*/

gen year2020=0
replace year2020=1 if year == 2020
*----------3.1:

teffects nnmatch (logmw pcp temp) (year2020) if year>2018, ematch(zon dow hour month) generate(nn_)

g logmw_hat = .
replace logmw_hat = 

*----------3.2:


*----------3.3:





exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1.
2.
3.


Version Control:


