# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:52:41 2021

@author: 16617

maximum likelihood estimate of parameter, p for binomial distribution

profile likelihood estimate of confidence interval for probability of
success

given a sample size and a value for alpha:
compute the profile likelihood bounds on estimats of p for that
sample size.   then given a hypothesized p_H0, computer the power of the 
test

"""

# clear variables and console
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import numpy as np
from os import chdir
import matplotlib.pyplot as plt
from scipy.stats import chi2, binom, norm, beta


# set this for your computer:
chdir('/Users/asherhanson/Desktop/')
#chdir('C:/Users/DrJ/Documents/Python Scripts/MaximumLikelihood')

# log likelihood
LL = lambda n,p,x: np.array(x*np.log(p) + (n-x)*np.log(1-p))

def LLfirth(n,p,x):
    nTrials = n
    xObs = n*p
    pF = (xObs+0.5)/(nTrials+1)
   
    return(np.array(x*np.log(pF) + (n-x)*np.log(1-pF)))
    
    
twoLogLike = lambda  llpStar, llp: 2*(llpStar-llp)

L = lambda p,x,n: p**x * (1-p)**(n-x) # likelihood
# likelihood ratio..pStar is MLE

lRatio = lambda p, pStar, x, n: L(p,x,n)/L(pStar,x,n)

pStarDensity = lambda p, pStar, x, n: \
    np.sqrt(2*np.pi*n/(pStar*(1-pStar)))*lRatio(p,pStar,x,n)
    
penalizedLogliHood = lambda xSuccess, xTrials: \
    np.log( xSuccess+0.5)/(xTrials+1)
    

def interpolate(PLsave, PLrange, chiSq):
    '''
    find values of  p  that are endpoints of the chisqCrit 
    confidence interval

    Parameters
    ----------
    PLsave : TYPE list
       list of the log likelihood ratio values
    range : list of the range of p-values
        DESCRIPTION.
    chiSqCrit : float
        critical value of Chi-Squared distribution, 1 dof

    Returns
    -------
    tuple of lower, upper Confidence interval values

    '''

    n = len(PLsave)
    minLocPLsave =  np.argmin(PLsave) 
    
    for i in range(1,(n-1)):
         if PLsave[i] <= chiSq:
            break
    
    LCL=0
    if i < minLocPLsave:
        LCL = -(PLsave[i-1]-chiSq)/(PLsave[i-1]-PLsave[i])* \
            (PLrange[i-1]-PLrange[i])+PLrange[i-1]
    else:
        LCL = (PLsave[i+1] - chiSq)/(PLsave[i+1]-PLsave[i])* \
            (PLrange[i+1]-PLrange[i])+PLrange[i]
    if LCL < 0: LCL=0
            
   
    for i in range((n-2),-1,-1):
        if PLsave[i] <= chiSq:
            break
    
    UCL = 1
    if i < minLocPLsave:  
        UCL = -(PLsave[i+1]-chiSq)/(PLsave[i+1]-PLsave[i])* \
            (PLrange[i+1]-PLrange[i])+PLrange[i]
    else:
        UCL = (PLsave[i-1]-chiSq)/(PLsave[i-1]-PLsave[i])* \
            (PLrange[i-1]-PLrange[i])+PLrange[i-1]
    
    if (UCL < LCL or UCL>1 or i==(n-2)): UCL = 1
       
    return  (LCL, UCL)


inputOK=False

while( not inputOK):
    nTrials = int(input('Enter (integer) sample size:  '))
    if (nTrials>1 and nTrials <= 200):
        alpha = float(input('Enter alpha (0 < alpha < 1): '))
        if 0 < alpha and alpha < 1:
            p_H0 = float(input('Enter hypothesized p '))
            if 0 < p_H0 and p_H0 < 1:
                xResult = int(input('Enter (integer) observed successes: '))
                if (xResult >=0 and xResult <= nTrials):  break
    else:
        print('try again: 1 < sample size  <= 200')
        print('0<alpha<1')

nTrialsFirth = nTrials + 1
confidenceVal = 1-alpha
confidenceValPL = 1-alpha
chiSqCritPL = chi2.ppf(confidenceValPL,1)

pSave = []  # list of probabilities
uclPL = []
lclPL = []

numPvalues = 6000
pValues = np.linspace(.5/numPvalues,1-0.5/numPvalues,num=numPvalues)

for xSuccess in range((nTrials)):
    
    #xSuccessF = xSuccess + 0.5
    
    #if xSuccess == 0:  xSuccess = 0.5
    #if xSuccess == nTrials: xSuccess = nTrials-0.5 
        
    #pStarF = xSuccessF/nTrialsFirth
    pStar  = xSuccess/nTrials
        
    logLStar = float(LLfirth(nTrials, pStar, xSuccess))
    
    # same as
    #logLstar = float(LLfirth( nTrials, pStar, xSuccess ))
    # print('pStar {}, logLStar {}'.format(pStar, logLStar))
     
    pSave.append(pStar)

    saveTwoL=[]

    for pV in pValues:
        pVtemp = pV
        
        #llp = float(LL(nTrials, pVtemp, xSuccess))
        llp = float(LLfirth(nTrials, pVtemp, xSuccess))
            
        twoL = twoLogLike(logLStar, llp)
        saveTwoL.append(twoL)
                                    
# find the CI

    LCL, UCL = interpolate(saveTwoL, pValues, chiSqCritPL)
    lclPL.append(LCL)
    uclPL.append(UCL)
    
plt.figure(1)
pRange = range((nTrials))
pVals = [float(x)/nTrials for x in pRange]
plt.plot(pVals, pSave, 'k', label='p MLE ')
plt.plot(pVals, lclPL, color='indigo', label = 'profile Likelihood',
         linestyle='dashed')
plt.plot(pVals, uclPL, color='indigo', linestyle='dashed')   
plt.title('Profile Likelihood Confidence Interval\nn={}, alpha= {}'.\
          format(nTrials, alpha))
plt.grid() 
plt.legend()
plt.show()


# for plotting
pAxis = np.linspace(start=0.5/(nTrials), stop=(nTrials-0.5)/(nTrials),
            num=1000)

#  We have p_H0 I want a PL CI about p_H0
p_H0successes = p_H0*nTrials
##logLikeP_H0 = LL(nTrials, p_H0, p_H0successes)
logLikeP_H0 = LLfirth(nTrials, p_H0, p_H0successes)

# get the (1-alpha) CI for p_H0; find power, confidence
saveTwoL = []

for p in pAxis:
    #llpALT = LL(nTrials, p, p_H0successes)
    llpALT = LLfirth(nTrials, p, p_H0successes)
    twoL = twoLogLike(logLikeP_H0, llpALT)
    saveTwoL.append(twoL)
    
p_H0lclPL, p_H0uclPL = interpolate(saveTwoL, pAxis, chiSqCritPL) 


# print('pStar: {},{}'.format(p_H0lclPS, p_H0uclPS))
llp = float(LLfirth(nTrials, p_H0, p_H0*nTrials))


# simulation for power of the test ---------------------

simSampleSize=5000

PLpowerTest = []

for j in range(len(pAxis)):
    pALT = pAxis[j]
    logLStar = float(LLfirth(nTrials, pALT, p_H0successes)) # assume H_A true
    # get a CI about p
    
    bSample = binom.rvs(nTrials, pALT, size= simSampleSize )/nTrials
   
    betaCountPL = 0
    
    #alphaCountPL = 0
    for i in range(simSampleSize):
        if(bSample[i] < p_H0uclPL and bSample[i] >  p_H0lclPL):
            betaCountPL +=1
    
    PLpowerTest.append(1-betaCountPL/simSampleSize)
    
## Alpha coverage --------------------------------------------

#here we recompute the CI for each pALT
    
PLalpha = []
  

alphaSampleSize = 1000

for j in range(len(pAxis)):
    pALT = pAxis[j]
    pALTsuccesses = pALT*nTrials
    
    logLStar = float(LLfirth(nTrials, pALT, pALTsuccesses)) # assume H_A true
    # get a CI about p
    
    bSample = binom.rvs(nTrials, pALT, size= alphaSampleSize )/nTrials
    
    
    # profile likelihood coverage
    
    pStar =  pALTsuccesses/nTrials
        
    logLStar = float(LLfirth(nTrials ,pStar, pALTsuccesses))
    # print('pStar {}, logLStar {}'.format(pStar, logLStar))
     
    saveTwoL=[]
    
    for pV in pAxis:
        
        llp = float(LLfirth(nTrials, pV, pALTsuccesses))
            
        twoL = twoLogLike(logLStar, llp)
        saveTwoL.append(twoL)
        
# find the CI for pALT

    pALTlclPL, pALTuclPL = interpolate(saveTwoL, pAxis, chiSqCritPL)
    
    
    alphaCountPL = 0  # profile likelihood    
    for i in range(alphaSampleSize):        
        if(bSample[i] <  pALTuclPL and bSample[i] >   pALTlclPL):
            alphaCountPL +=1 
            
    PLalpha.append(np.mean(alphaCountPL)/alphaSampleSize)        
    
 
# confidence coveage plots
plt.figure(2)
plt.plot(pAxis, PLalpha, color='indigo', label='profile likelihood')
plt.axhline((1-alpha), 0.02, 0.98, color='red', linestyle=':')
plt.grid()
#plt.title('confidence level')
plt.title('Confidence for alpha = {}, p_H0 = {}, {} trials'.
          format(alpha, p_H0, nTrials))
plt.xlabel('probabilty of success')
plt.ylabel('Confidence')
plt.legend()
plt.show()
    

plt.figure(3)  
plt.plot(pAxis, PLpowerTest, 'b', label='Profile Likelihood')
plt.grid()
plt.title('Power of the test for alpha = {}, p_H0 = {}, {} trials {} successes'. \
          format(alpha, p_H0, nTrials, xResult))
plt.title(('Profile Likelihood: Power of the test\n \
           {} trials alpha={}, p_H0 = {}'.format(nTrials,alpha, p_H0)))
plt.xlabel('probability, p')
plt.ylabel('power')
plt.legend()
plt.show()
    
##  confidence for p_H0

print('\n\n============================================')
print('\nSample size {}, desired alpha={}, test p_H0 = {}'.\
      format(nTrials, alpha, p_H0))
print('observed successes = {}'.format(xResult))

print('Profile Likelihood CI for {}: ({}, {})'.format(p_H0, 
        round(p_H0lclPL,3), round(p_H0uclPL,3)))

 
## confidence interval test:
bSample = binom.rvs(nTrials, p_H0, size=simSampleSize)/nTrials
alphaCountPL = 0

for i in range(simSampleSize):
    if (bSample[i] >= p_H0lclPL and bSample[i] <= p_H0uclPL): alphaCountPL += 1   
    
alphaPL = 1-alphaCountPL/simSampleSize

## ---operational test: only integer successes ---------------
xResult = 5
nTrials = 9
p_H0 = 0.95
simSampleSize = 5000


pRange = range((nTrials+1))

# only possible observed results
pVals = [float(x)/nTrials for x in pRange]
#pVals

PLpowerTest = []
p_H0successes = p_H0*nTrials  # based on true value of p

alphaCountPL = 0  # profile likelihood alpha

# xResult is observed number of successes
pResult = xResult/nTrials

#  bSample = binom.rvs(nTrials, p_H0, size=simSampleSize)/nTrials
bsample = binom.rvs(nTrials, pResult, size = simSampleSize)/nTrials 

for i in range(simSampleSize):
    if (bSample[i] >= p_H0lclPL and bSample[i] <= p_H0uclPL):
        alphaCountPL += 1 
    
alphaPL = 1-alphaCountPL/simSampleSize
    
print('\nProfile Likelihood:  alpha: {}, estimated from sim: {}'. \
      format(alpha, round(alphaPL,3)))
print('   if one-sided test, alpha = {}'.format(round(2*alphaPL,3)))

for i in range(len(pVals)):
    pALT = pVals[i]
    logLStar = float(LLfirth(nTrials, pALT, p_H0successes)) # assume H_A true
    # get a CI about p
    
    bSample = binom.rvs(nTrials, pALT, size= simSampleSize )/nTrials
    betaCountPL = 0
    
    for i in range(simSampleSize):
        if(bSample[i] <= p_H0uclPL and bSample[i] >=  p_H0lclPL):
            betaCountPL +=1
    PLpowerTest.append(1-betaCountPL/simSampleSize)

plt.figure(4)
plt.scatter(pVals, PLpowerTest,marker=1, color='blue', label = 'profile likelihood')
plt.title('Power of the test for alpha = {}\np_H0 = {}, {} trials'.
          format(alpha, p_H0, nTrials))
plt.xlabel('probability of success, p')
plt.ylabel('power')

plt.legend()
plt.grid()
plt.show()
