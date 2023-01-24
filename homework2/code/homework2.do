clear all
set more off

import delimited "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-db\homework2\kwh.csv"

local outputpath = "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework2\output" 
	
	cd "`outputpath'"

lab var electricity "Electricity Consumption (Kwh)"
lab var sqft "Square Feet"
lab var retrofit "Retrofit"
lab var temp "Temperature (F)"
	
	
eststo treated: quietly estpost summarize electricity-temp if retrofit==1
eststo control: quietly estpost summarize electricity-temp if retrofit==0
eststo diff: quietly estpost ttest electricity-temp, by(retrofit) unequal
esttab treated control diff using comparison.tex, tex cells((mean(fmt(2) label(Mean)) sd(fmt(2) par label(Std. Dev.)) b(star pattern(0 0 1) fmt(3) label(T-stat.)) t(pattern(0 0 1) par fmt(3) label(p-value)))) replace

set scheme plotplainblind, permanently

tw scatter electricity sqft

eststo regression: reg electricity retrofit sqft temp, vce(robust)

outreg2 regression using statafrag, tex(frag) replace