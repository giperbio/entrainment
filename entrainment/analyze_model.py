import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
import statsmodels.api as sm
from box import Box
from collections import namedtuple
from scipy import stats

def analyze_model(
    model, exposure, param = "tau", name = None, print_stats = True, plot = True
    ):
    """Compute and plot model statistics."""
    data = [i[param] for i in np.array(model.turtles[exposure])]
    
    out = Box(
        mean = np.mean(data), var = np.var(data), std = np.std(data), 
        min = np.quantile(data, 0), q_1 = np.quantile(data, 0.25), 
        median = np.quantile(data, 0.5), q_3 = np.quantile(data, 0.75), 
        max = np.quantile(data, 1), kurtosis = stats.kurtosis(data),
        skew = stats.skew(data), kstest = stats.kstest(data, stats.norm.cdf), 
        shapiro = stats.shapiro(data)
        )
    
    if print_stats == True: print_model_analysis(out, exposure, name)
    if plot == True: plot_model_analysis(data, exposure, name)
    
    return out

def print_model_analysis(stats, exposure, name = None):
    line = "---------------------------------------------------------"
    
    title = ("[Group: {name} | Exposure: {exposure}]")\
             .format(name = name, exposure = exposure.title())
    
    summary = ("Mean = {mean}\nVar. = {var}\nSD = {std}\n\n" +\
               "Min. = {min}\n1st Qu. = {q_1}\nMedian = {median}\n" +\
               "3rd Qu. = {q_3}\nMax. = {max}\n\n" +\
               "Kurtosis = {kurtosis}\nSkewness = {skew}\n\n" +\
               "Kolmogorov-Smirnov test p-value = {kstest}\n" +\
               "Shapiro-Wilks test p-value = {shapiro}")\
               .format(
                   mean = stats.mean, var = stats.var, std = stats.std,
                   min = stats.min, q_1 = stats.q_1, median = stats.median,
                   q_3 = stats.q_3, max = stats.max, kurtosis = stats.kurtosis,
                   skew = stats.skew, kstest = stats.kstest.pvalue,
                   shapiro = stats.shapiro.pvalue
                   )
    
    print(line, title, summary, line, sep = "\n\n")
    
    return None

def plot_model_analysis(
    data, exposure, name = None, dist = scipy.stats.distributions.norm
    ):
    title = ("Group = {name}, Exposure = {exposure}, Mean = ${mean}$, " +\
             "KS = ${kstest}$, Shapiro-Wilk = ${shapiro}$")\
             .format(
                 name = name, exposure = exposure.title(), 
                 mean = round(np.mean(data), 3),
                 kstest = round(stats.kstest(data, stats.norm.cdf).pvalue, 3),
                 shapiro = round(stats.shapiro(data).pvalue, 3)
                 )
    
    plt.rcParams.update({'font.size': 8})
    plt.clf()
    
    fig, [ax_x, ax_y] = plt.subplots(nrows = 1, ncols = 2)
    
    ax_x.hist(data, density = True, edgecolor = "white", color = "#bcbcbc")
    sns.kdeplot(
        data, ax = ax_x, color = "red", linewidth = 1, warn_singular = False
        )
    ax_x.set_xlabel("$\\tau$")
    ax_x.set_ylabel("Frequency")
    
    sm.qqplot(
        np.array(data), ax = ax_y, dist = dist, line = "s", marker = "o", 
        markerfacecolor = "None", markeredgecolor = "black",
        markeredgewidth = 0.5
        )
    ax_y.set_xlabel("Theoretical quantiles (Std. normal)")
    ax_y.set_ylabel("Sample quantiles ($\\tau$)")
    ax_y.set_xlim(-3.5, 3.5)
    
    plt.suptitle(title, fontsize = 8, y = 0.9375)
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.10625, bottom = 0.1625, right = 0.95, top = 0.875,
        wspace = 0.4, hspace = None
        )
    plt.show()
    
    return None
