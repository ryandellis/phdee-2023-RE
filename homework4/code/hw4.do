/*==================================================
project:       
Author:        Ryan Ellis 
E-email:       
url:           
Dependencies:  
----------------------------------------------------
Creation Date:    20 Feb 2023 - 21:03:32
Modification Date:   
Do-file version:    01
References:          
Output:             
==================================================*/
clear all
set more off
/*==================================================
              0: Program set up
==================================================*/
version 17
drop _all
import delimited "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4\bycatch_stata.csv"
local outputpath "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4\output"
cd "`outputpath'"

/*==================================================
              1: Fixed Effects Regressions
==================================================*/


*----------1.1: Stata will create indicators for us within the regression syntax
drop const
xtset firm month
reg bycatch treated shrimp salmon firmsize i.firm i.month, vce(cluster firm)
estimates store model1


*----------1.2: "the hard way"
su firm
local firms = `r(max)'
tab month, g(month)
local vars "firmsize treated shrimp salmon bycatch month2 month3 month4 month5 month6 month7 month8 month9 month10 month11 month12 month13 month14 month15 month16 month17 month18 month19 month20 month21 month22 month23 month24"

foreach x of local vars {
	gen `x'_w = .
	forvalues f = 1/`firms' {
	su `x' if firm == `f'
	replace `x'_w = `x' - `r(mean)' if firm == `f'
	
	}
}	
reg bycatch_w treated_w shrimp_w salmon_w firmsize_w i.month, vce(cluster firm)


*similarly, you could use *xtreg, fe* for within estimation

xtreg bycatch treated shrimp salmon firmsize i.month, fe vce(cluster firm)
estimates store model2
*----------1.3:

outreg2 [model1 model2] using "stata_table_hw4.tex", replace keep(treated shrimp salmon firmsize) tex(frag) label ctitle("Firm indicators" "Within-transformation")



exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1.
2.
3.


Version Control:


