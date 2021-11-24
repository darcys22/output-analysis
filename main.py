#!/home/sean/python/default/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import stats, optimize, interpolate
import os

OUTPUT_FILES_DIRECTORY = "data"
OUTPUT_DATABASE_FILENAME = f'output_data/output_aggregation.csv'
ANALYSED_OUTPUT_DATABASE_FILENAME = f'output_data/analysed_output_data.csv'
CURRENT_BLOCKCHAIN_HEIGHT = 692678

LIST_OF_DISTS = ['alpha','anglit','arcsine','beta','betaprime','bradford','burr','burr12','cauchy','chi','chi2','cosine','dgamma','dweibull','erlang','expon','exponnorm','exponweib','exponpow','f','fatiguelife','fisk','foldcauchy','foldnorm','genlogistic','genpareto','gennorm','genexpon','genextreme','gausshyper','gamma','gengamma','genhalflogistic','gilbrat','gompertz','gumbel_r','gumbel_l','halfcauchy','halflogistic','halfnorm','halfgennorm','hypsecant','invgamma','invgauss','invweibull','johnsonsb','johnsonsu','kstwobign','laplace','levy','levy_l','logistic','loggamma','loglaplace','lognorm','lomax','maxwell','mielke','nakagami','ncx2','ncf','nct','norm','pareto','pearson3','powerlaw','powerlognorm','powernorm','rdist','reciprocal','rayleigh','rice','recipinvgauss','semicircular','t','triang','truncexpon','truncnorm','tukeylambda','uniform','vonmises','vonmises_line','wald','weibull_min','weibull_max']

def get_output_data():
    return pd.read_csv(OUTPUT_DATABASE_FILENAME, delimiter=',')

def process_output_file(f):
    outputs = []
    collecting = False
    for line in f:
        if 'Amount' in line:
            collecting = True
        elif 'Min block height' in line:
            return outputs
        elif collecting:
            outputs.extend(line.split())

def build_output_db():
    all_outputs = []
    for filename in os.listdir(OUTPUT_FILES_DIRECTORY):
       with open(os.path.join(OUTPUT_FILES_DIRECTORY, filename), 'r') as f: # open in readonly mode
           all_outputs.extend(process_output_file(f))
    output_db = pd.DataFrame(all_outputs, columns=["Height"])
    print(output_db.head())
    output_db.to_csv(OUTPUT_DATABASE_FILENAME)
    return output_db

def analyse_output_db(output_database):

    results = []
    for i in LIST_OF_DISTS:
        dist = getattr(stats, i)
        param = dist.fit(CURRENT_BLOCKCHAIN_HEIGHT - output_database["Height"])
        a = stats.kstest(CURRENT_BLOCKCHAIN_HEIGHT - output_database["Height"], i, args=param)
        results.append((i,a[0],a[1]))

    results.sort(key=lambda x:float(x[2]), reverse=True)
    # for j in results:
        # print("{}: statistic={}, pvalue={}".format(j[0], j[1], j[2]))

    analysed_output_db = pd.DataFrame.from_records(results, columns=["Distribution Name", "Statistic", "PValue"])
    analysed_output_db.to_csv(ANALYSED_OUTPUT_DATABASE_FILENAME)

    dist = getattr(stats, results[0][0])
    parameters = dist.fit(CURRENT_BLOCKCHAIN_HEIGHT - output_database["Height"])
    print("")
    print("")
    print("")
    print("")
    print("Best fitting distribution is: {}".format(results[0][0]))
    print("-----------")
    print(parameters)

    x = np.linspace(0,CURRENT_BLOCKCHAIN_HEIGHT,1000)
    fitted_data = dist.pdf(x, parameters[0], parameters[1], parameters[2])

    plt.hist(CURRENT_BLOCKCHAIN_HEIGHT - output_database["Height"], density=True)

    plt.plot(x,fitted_data,'r-')
    plt.savefig("fitted_histogram.png", bbox_inches="tight")

if __name__ == '__main__':
    # Build the output database and save to disk
    # output_db = build_output_db()
    output_db = get_output_data()
    analyse_output_db(output_db)



