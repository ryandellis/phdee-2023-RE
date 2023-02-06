clear all
set more off


import delimited "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-db\homework2\kwh.csv"

local outputpath = "C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework3\output" 
	
	cd "`outputpath'"

set scheme plottigblind
	
g ln_elec = ln(electricity)
g ln_sqft = ln(sqft)
g ln_temp = ln(temp)
g retro_mfx = .
g sqft_mfx = .
g temp_mfx = .

lab var electricity "Electricity Consumption (Kwh)"
lab var sqft "Square Feet"
lab var retrofit "Retrofit"
lab var temp "Temperature (F)"
lab var ln_elec "ln(Electricity, Kwh)"
lab var ln_sqft "ln(Square Feet)"
lab var ln_temp "ln(Temperature (F))"
lab var retro_mfx "Marginal Effects, retrofit"
lab var sqft_mfx "Marginal Effects, sqft"
lab var temp_mfx "Marginal Effects, temp"


*Bootstrapping using guidance from hw1 sample code:

mat betas = J(1000,4,.) // pre-allocate a matrix for the outcomes of our 1000 regressions
mat mfx = J(1000, 3,.)

program define bootstrapsample, eclass
		forvalues i = 1/1000 {
			preserve // preserves the data as it was in the memory at this point
				bsample // samples with replacement up to the number of observations
				
				reg ln_elec retrofit ln_sqft ln_temp // main regression

				mat betas[`i',1] = _b[retrofit] // filling matrix "betas" with results
				mat betas[`i',2] = _b[ln_sqft]
				mat betas[`i',3] = _b[ln_temp]
				mat betas[`i',4] = _b[_cons]
				
				replace retro_mfx = ((exp(_b[retrofit]) - 1)*electricity)/(exp(_b[retrofit])^retrofit) // generating marginal effects
				replace sqft_mfx = (_b[ln_sqft]*electricity)/sqft
				replace temp_mfx = (_b[ln_temp]*electricity)/temp
				
				su retro_mfx
				mat mfx[`i',1] = r(mean)
				su sqft_mfx
				mat mfx[`i',2] = r(mean)
				su temp_mfx
				mat mfx[`i',3] = r(mean)
				
				
			restore

		}
		
					
		
		svmat double betas
		svmat double mfx

	corr betas1 betas2 betas3 betas4, cov
	mat C = r(C)
	drop betas*

	reg ln_elec retrofit ln_sqft ln_temp // rerun the regression
	ereturn repost V = C
end

bootstrapsample // run program
estimates store bootreg

rename mfx1 mfx_retro
lab var mfx_retro "Marginal Effects, Retrofit"
rename mfx2 mfx_sqft
lab var mfx_sqft "Marginal Effects, Square Feet"
rename mfx3 mfx_temp
lab var mfx_temp "Marginal Effects, Temperature (F)"

mean mfx_retro mfx_sqft mfx_temp
estimates store marg_fx

etable, estimates(bootreg marg_fx) cstat(_r_b) cstat(_r_ci) center column(index) varlabel title("Regression results and Marginal Effects") export(hw3table.tex) replace

coefplot marg_fx, drop(mfx_retro) ci(95) vertical title("Average Marginal Effects")
graph export ame_hw3.png, replace
