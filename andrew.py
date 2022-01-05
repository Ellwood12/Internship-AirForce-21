# %%
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.optimize as opt
from scipy.interpolate import BSpline
np.seterr(divide='ignore')


# %%
class binom_conf():

    def __init__(self,x,n,alpha=0.05):
        self.x = x + .5
        self.n = n + 1
        self.mle = np.array(self.x/self.n)
        self.alpha = alpha
        #print(self.x)

    def loglike(self,p):
        res = self.x * math.log(p) + (self.n-self.x) * math.log(1-p)
        return(res)

    def prof_like(self):
        zero = self.loglike(self.mle) - .5 * stats.chi2.ppf(1-self.alpha,1)
        f = lambda p: self.loglike(p)-zero
        print(f)
        if self.x <= .5:
            lb = 0
        else:
            lb = opt.brentq(f,0,self.mle)
#        if self.n - self.x <= .5:
#            ub = 1
#        else:
#            ub = opt.brentq(f,1,self.mle)
#        return(lb,ub)
# %%
try_1 = binom_conf(1,1)
try_1.__init__(x=4,n=8)
#try_1.loglike(p=0.3)
try_1.prof_like()
# %%

#class binom_power():
#    def __init__(self, nTrials, alpha = 0.05, p_HO = 0.5, nsample = 1000, num =500):
#        self.p_support = np.linspace(0,1,num,num)
#        self.nTrials = nTrials
#        self.alpha = alpha
#        self.p_HO = p_HO
#        self.fit(nsample)
        #Where does fit come from?
# %%

#thing = binom_power(0)

# %%
