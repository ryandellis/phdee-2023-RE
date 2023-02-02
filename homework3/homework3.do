clear all
set more off


import delimited "C:\Users\rellis63\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-db\homework2\kwh.csv"

local outputpath = "C:\Users\rellis63\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework3\output" 
	
	cd "`outputpath'"


	
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


*initial regression and marginal effects

reg ln_elec retrofit ln_sqft ln_temp
estimates store og_betas


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






/*program define bootstrapsample, eclass
		forvalues i = 1/1000 {
			preserve // preserves the data as it was in the memory at this point
				bsample // samples with replacement up to the number of observations
				
				reg ln_elec retrofit ln_sqft ln_temp

				mat betas[`i',1] = _b[retrofit]
				mat betas[`i',2] = _b[ln_sqft]
				mat betas[`i',3] = _b[ln_temp]
				mat betas[`i',4] = _b[_cons]
			restore // restores the data as you preserved it originally
				
				
				
		}

svmat double betas, names(bootbeta)

rename bootbeta1 retro_bst
rename bootbeta2 ln_sqft_bst
rename bootbeta3 ln_temp_bst
rename bootbeta4 ln_cons_bst

corr retro_bst ln_sqft_bst ln_temp_bst ln_cons_bst, cov // get the covariance matrix
	
mat A = r(C) // save covariance matrix
drop retro_bst ln_cons_bst ln_temp_bst ln_cons_bst
				
reg ln_elec retrofit ln_sqft ln_temp // rerun the regression
ereturn repost V = A

end

bootstrapsample
estimates store bootreg
ereturn display

reg ln_elec retrofit ln_sqft ln_temp
reg ln_elec retrofit ln_sqft ln_temp, vce(bootstrap, reps(1000))


/*bootstrapping with guidance from ChatGPT:

// Create new variables to store bootstrapped estimates
gen boot_intercept = .
gen boot_retrofit = .
gen boot_sqft = .
gen boot_temp = .
gen boot_ame_retrofit = .
gen boot_ame_sqft = .
gen boot_ame_temp = .

// Number of bootstrap replications
local B = 1000

// Bootstrapping loop
forvalues i = 1/`B' {
    
    // Resample the data with replacement
    bootstrap ln_elec retrofit sqft temp, seed(`i')
    
    // Estimate the regression coefficients
    reg ln_elec retrofit sqft temp, robust
    
    // Store the estimates for the intercept and independent variables
    replace boot_intercept = _b[_cons] if _n == `i'
    replace boot_retrofit = _b[retrofit] if _n == `i'
    replace boot_sqft = _b[sqft] if _n == `i'
    replace boot_temp = _b[temp] if _n == `i'
    
    // Calculate the average marginal effects
    // scalar ame_retrofit = exp(r(mean) + boot_retrofit*r(mean_retrofit)) - exp(r(mean))
    // scalar ame_sqft = exp(r(mean) + boot_sqft*r(mean_sqft)) - exp(r(mean))
    // scalar ame_temp = exp(r(mean) + boot_temp*r(mean_temp))- exp(r(mean))

    
    // Store the estimates for the average marginal effects
    replace boot_ame_retrofit = `ame_retrofit' if _n == `i'
    replace boot_ame_sqft = `ame_sqft' if _n == `i'
    replace boot_ame_temp = `ame_temp' if _n == `i'
}

// Calculate the lower and upper bounds of the 95% confidence intervals
sort boot_intercept
local lower_intercept = boot_intercept[`floor(0.025*`B')']
local upper_intercept = boot_intercept[`floor(0.975*`B')']
sort boot_retrofit
local lower_retrofit = boot_retrofit[`floor(0.025*`B')']
local upper_retrofit = boot_retrofit[`floor(0.975*`B')']
sort boot_sqft
local lower_sqft = boot_sqft[`floor(0.025*`B')']
local upper_sqft = boot_sqft[`floor(0.975*`B')']
