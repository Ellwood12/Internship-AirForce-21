# -*- coding: utf-8 -*-
"""
Created on Tue May 25 11:33:19 2021
 
@author: 1556543727C
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.optimize as opt
import pandas as pd
from scipy.interpolate import BSpline
np.seterr(divide='ignore')
 
class binom_conf():
    """
    Generates confidence interval estimates for the probability of a binomial
    random variable. Uses Wald estimate and Profile likelihood techniques to
    calculate confidence intervals.
   
    The formula used for Wald estimates is:
        \hat{p} +- Z_{1-alpha/2}*\sqrt(\hat{p}(1-\hat{p})/n)
   
    The Formula used for Profile likelikhood is:
        loglikelihood_binom(p) -.5*\chisq(1-alpha,1) = 0
   
    Inputs:
    x = number of successes in a sample. Can be an arrary of multiple outcomes
    n = number of bernoli trails in a sample. If arrary each element corresponds
    to an element in x
    alpha = Type I error rate
    firth_all = Apply Firths Maximum Likelihood Bias Reduction adding to n and
    .5 to x
   
    Outputs:
    A Pandas DataFrame with the lower and upper bounds for the confidence
    intervals
   
    Example:
   
        x = np.arange(nTrials+1)
       n = np.repeat(nTrials,nTrials+1)
       
        conf = binom_conf(x,n,alpha,firth_all=False).fit()
        print(conf)
       
    
    """
    def __init__(self,x,n,alpha=.05,firth_all=False,upper_tail =None):
       
        # Do a firths correction if x = 0 or n
        self.x = np.atleast_1d(np.asarray(x,dtype=np.float))
        self.n = np.atleast_1d(np.asarray(n,dtype=np.float))
       
        if firth_all is not None:
            if firth_all:
                index = np.ones(self.x.shape[0],dtype=bool)
            else:
                index = np.logical_or(self.x == 0,self.x == n)
   
            self.x[index] = self.x[index] + .5
            self.n[index] = self.n[index] + 1
       
        self.mle = np.array(self.x/self.n)
        if upper_tail is None:
            self.alpha = alpha
        else:
            self.alpha = alpha*2
       
        self.upper_tail = upper_tail
   
    @staticmethod
    def loglike(p,x,n):
        if x==0:
            res = (n-x)*np.log(1-p)
        elif n-x == 0:
            res = x*np.log(p)
        else:
            res = x*np.log(p)+(n-x)*np.log(1-p)
        return(res)
       
        
    def prof_like(self,i):
        zero = self.loglike(self.mle[i],self.x[i],self.n[i]) - .5*stats.chi2.ppf(1-self.alpha,1)
        f = lambda p: self.loglike(p,self.x[i],self.n[i])-zero
       
        if self.x[i] <=.5:
            lb = 0
        else:
            lb = opt.brentq(f,0,self.mle[i])
        if self.n[i] - self.x[i]  <= .5:
            ub = 1
        else:
            ub = opt.brentq(f,1,self.mle[i])
           
        if self.upper_tail is not None:
            if self.upper_tail == True:
                ub = 1
            else:
                lb = 0
        return(lb,ub)
       
    def wald(self,i):
        sdWald = np.sqrt(self.ci[i,0]*(1-self.ci[i,0])/self.n[i])
        seWald = sdWald*stats.norm.ppf((1-self.alpha/2))
        lb = np.maximum(0.,self.ci[i,0] - seWald)
        ub = np.minimum(1.,(self.ci[i,0] + seWald))
        return(lb,ub)
       
    def bayes(self,i):
        '''
        This works but slows down the power calcs so isn't included
        '''
        m = .5
        if self.x[i] % 1 == .5:
            m = 0
        f = lambda p: p**(self.x[i]+m)*(1-p)**(self.n[i]+m-self.x[i])
        p_s = np.linspace(0,1,10000)
        postier = f(p_s)
        postier = f(p_s)/np.sum((p_s[1]-p_s[0])*f(p_s))
        index = np.flip(np.argsort(postier))
        ut = np.triu((p_s[1]-p_s[0])*np.ones((postier.shape[0],postier.shape[0])))
        thing = index[np.dot(postier[index],ut) < 1-self.alpha]
        hdr = p_s[thing]
        lb = np.min(hdr)
        ub = np.max(hdr)
        return(lb,ub)
           
    def fit(self):
        self.ci = np.zeros((self.x.shape[0],5))
        for i in range(self.x.shape[0]):
            self.ci[i,0] = self.mle[i]
            #Profile Likelihood
            self.ci[i,1:3] = self.prof_like(i)
            # Wald
            self.ci[i,3:5] = self.wald(i)
        self.ci = pd.DataFrame(self.ci)
        self.ci.columns = ['P_MLE',
                           'Lower Bound PL',
                           'Upper Bound PL',
                           'Lower Bound Wald',
                           'Upper Bound Wald']
        return(self.ci)
       
        
class binom_power():
    """
   
    """
    def __init__(self,nTrials,alpha=.05,p_H0=.5,nsample=1000,num=500):
        self.p_support = np.linspace(0,1,num=num)
        self.nTrials = nTrials
        self.alpha = alpha
        self.p_H0 = p_H0
       
        self.fit(nsample)
       
    def fit(self,nsample=1000,firth_all = False,upper_tail = None):
        self.pRange = range((self.nTrials+1))
        self.x = np.arange(self.nTrials+1)
        self.n = np.repeat(self.nTrials,self.nTrials+1)
        self.conf = binom_conf(self.x,self.n,self.alpha,
                               firth_all=firth_all,upper_tail=upper_tail).fit()
        self.conf = pd.DataFrame(self.conf)
        self.power(nsample)
   
    def power(self,nsample=1000):
        self.power_prof = np.zeros(self.p_support.shape[0])
        self.power_wald = np.zeros(self.p_support.shape[0])
        self.confidence_prof = np.zeros(self.p_support.shape[0])
        self.confidence_wald = np.zeros(self.p_support.shape[0])
 
        for i in range(self.p_support.shape[0]):
            s = stats.binom.rvs(self.nTrials, self.p_support[i], size= nsample )
 
            # Power for Profile Likelihood
            res = np.logical_and(self.conf.iloc[s,1] < self.p_H0,self.conf.iloc[s,2] >self.p_H0)
            self.power_prof[i] = 1-np.sum(res)/nsample
 
            # Power for Wald
            res = np.logical_and(self.conf.iloc[s,3] <self.p_H0,self.conf.iloc[s,4] >self.p_H0)
            self.power_wald[i] = 1-np.sum(res)/nsample
 
            # Confidence for Profile Likelihood
            res = np.logical_and(self.conf.iloc[s,1] <=self.p_support[i],self.conf.iloc[s,2] >=self.p_support[i])
            self.confidence_prof[i] = np.sum(res)/nsample
 
            # Confidence for Wald
            res = np.logical_and(self.conf.iloc[s,3] <=self.p_support[i],self.conf.iloc[s,4] >=self.p_support[i])
            self.confidence_wald[i] = np.sum(res)/nsample
        
    def plot_limits(self,title=None):
        plt.figure(figsize=(9,7))
       
        plt.plot(self.pRange,self.conf['P_MLE'], 'k', label='p MLE ')
        plt.plot(self.pRange,self.conf['Lower Bound PL'],
                 color='dodgerblue',linestyle = '--',
                 label = '{}% CI Profile Likelihood'.format(round((1-self.alpha)*100)))
        plt.plot(self.pRange,self.conf['Upper Bound PL'],
                 color='dodgerblue',linestyle = '--' )
        plt.plot(self.pRange,self.conf['Lower Bound Wald'],
                 color='orange',linestyle = '--',
                 label = '{}% CI Wald'.format(round((1-self.alpha)*100)))
        plt.plot(self.pRange,self.conf['Upper Bound Wald'],
                 color='orange',linestyle = '--')
        if title is None:
            title = '{}% Confidence intervals\nn={}'.format((1-self.alpha)*100, self.nTrials)
        plt.title(title)
        plt.grid()
        plt.legend()
        plt.xlabel('Number of successes')
        plt.ylabel('P')
        plt.show()
       
    def plot_power(self,axis=(None,None,None,None),figsize=None,title=None):
        if figsize is not None:
            plt.figure(figsize=figsize)
        plt.plot(self.p_support, self.power_prof, label='Profile Likelihood',color='dodgerblue')
        plt.plot(self.p_support, self.power_wald, label='Wald',color='orange')
        plt.axhline(y = self.p_H0, color = 'r', linestyle = 'dashed')
        plt.grid()
        if title is None:
            title = 'Power of the test, {} trials\n alpha={}, p_H0 = {}'.\
                format(self.nTrials, self.alpha, self.p_H0)
        plt.title(title)
        plt.xlabel('probability of success, p')
        plt.ylabel('power')
        plt.legend()
        plt.xlabel('True P')
        plt.ylabel('Power')
        plt.axis(axis)
        plt.show()
       
    def plot_confidence(self,axis=(None,None,None,None),figsize=None,title=None):
        if figsize is not None:
            plt.figure(figsize=figsize)
        plt.plot(self.p_support, self.confidence_prof, label='Profile Likelihood',color='dodgerblue')
        plt.plot(self.p_support, self.confidence_wald, label='Wald',color='orange')
        plt.grid()
        if title == None:
            title = 'Confidence of the test, {} trials\n alpha={}'.\
                format(self.nTrials, self.alpha)
        plt.title(title)
        plt.xlabel('probability of success, p')
        plt.ylabel('confidence')
        plt.axhline(1-self.alpha,c='red',label="Desired Confidence",linestyle='--')
        plt.legend()
        plt.xlabel('True P')
        plt.ylabel('Confidence')
        plt.axis(axis)
        plt.show()
