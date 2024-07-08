
import random
import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import seaborn as sns
# import matplotlib
# import matplotlib.pyplot as plt

from timeit import default_timer as timer

def fit_best(dataset):
        
        # Distributions to check
    # DISTRIBUTIONS = [        
       # st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
       # st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
       # st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
       # st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
       # st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
       # st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
       # st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
       # st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
       # st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
       # st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy]
    
    # Distributions to check
    DISTRIBUTIONS=[
        st.norm,st.pearson3, st.uniform,st.halflogistic,st.halfnorm
        ]
    
    # Create models from data
    # def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(dataset, bins=b, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0
    
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    
    # Estimate distribution parameters from data
    
    """For many distributions this might take a lot of time"""
    
    for distribution in DISTRIBUTIONS:
    
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
    
                # fit dist to data
                #Distribution Fitting with Sum of Square Error (SSE)
                params = distribution.fit(dataset)
    
    
                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]
    
                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
    
                print (distribution.name, [round(p,3) for p in params])
    
                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse
        except Exception:
            pass
    
    print ("BEST:",(best_distribution.name, [round(p,3) for p in best_params]),"\n")
    return (best_distribution.name,best_params)


if __name__ == "__main__":  
    
    unif_data=[]
    
    data_samples=100000
    
    range_inf = 0
    range_sup = 100
    b=100
    
    for el in range(data_samples):
        unif_data.append(random.randint(range_inf,range_sup))
        
    mu, sigma = (range_inf+range_sup)/2, 4 # mean and standard deviation
    normal_data = np.random.normal(mu, sigma, data_samples)



    y_df = pd.DataFrame(unif_data, columns=['Data'])
    print(y_df.describe(),"\n")
    y_df = pd.DataFrame(normal_data, columns=['Data'])
    print(y_df.describe(),"\n")
    
    

    ax = sns.distplot(unif_data,
                      bins=b,
                      kde=True,
                      color='blue',
                      hist_kws={"linewidth": 18,'alpha':1})
    ax = sns.distplot(normal_data,
                      bins=b,
                      kde=True,
                      color='red',
                      hist_kws={"linewidth": 18,'alpha':1})
    
    ax.set(xlabel='Distribution ', ylabel='Frequency')
    
    cpu=timer()
    fit_best(unif_data)
    
    #PROBABILITY for unif_data is simply 1 over samplesize
    
    prm = fit_best(normal_data)[1]
    
    #If I want probability for future values
    
    for i in range(range_inf+35,range_sup-35):
        print("value:",i,"probab:",st.norm(prm[0],prm[1]).pdf(i))
        
    print("Elapsed standard:",round(timer()-cpu,2),"s")
    
    cpu=timer()

    fit_best([i for i in unif_data if random.randint(0,1)%2==0])
    
    #PROBABILITY IF UNIFORM IS SIMPLY 1/samplesize
    
    prm = fit_best([i for i in normal_data if random.randint(0,1)%2==0])[1]
    
    # for i in range(range_inf+35,range_sup-35):
    #     print("value:",i,"probab2:",st.norm(prm[0],prm[1]).pdf(i))
        
    print("Elapsed filtered:",round(timer()-cpu,2),"s")
    