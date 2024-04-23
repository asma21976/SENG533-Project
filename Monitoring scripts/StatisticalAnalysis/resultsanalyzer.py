import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# for anova
from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

MICROSERVICE_TESTS = {
    "auth": "Authentication",
    "webhvy": "WebUI Heavy Use",
    "weblgt": "WebUI Light Use",
}

SCALING_TESTS = {
    "inst1": "1 Instance",
    "inst2": "2 Instances",
    "inst3": "3 Instances",
}

def load_data(filename):
    df = pd.read_csv(filename, header=None)
    df= df.replace(-1, pd.NA)
    return df

def generate_figures_for_test(data_list, data_labels, figure_name):
    plt.boxplot(data_list, labels=data_labels, showfliers=False)
    plt.xlabel("Distributions")
    plt.ylabel("Response Times")
    plt.title(f"Box Plots Comparing {figure_name} Distributions")

    # Save the box plot as a PNG file
    plt.tight_layout()
    plt.savefig(f"results_statistics/Boxplot_{figure_name.replace(' ', '_')}.png")
    plt.close()

    # Lectures say to use histogram intervals = avg sqrt of the # of samples for each distribution
    avg_sqrt_samples = np.mean([np.sqrt(len(data)) for data in data_list])

    # we are using less number of bins to make figure less ragged
    num_bins = int(round(avg_sqrt_samples) / 3)

    # make a figure showing the histograms of each distribution
    fig, axes = plt.subplots(len(data_list), 1, figsize=(7, 2 * len(data_list)))
    for i, data in enumerate(data_list):
        axes[i].hist(data, bins=num_bins)
        axes[i].set_title(f'Histogram for {figure_name} Distribution {data_labels[i]}')
        axes[i].set_xlabel('Values')
        axes[i].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(f"results_statistics/Histograms_{figure_name.replace(' ', '_')}.png")
    plt.close()

    return

def perform_experiment_analysis(df, scaling_test=False):
    for key in MICROSERVICE_TESTS:
        print(f"\n\nStarting {key} Test Analysis")
        # Separate test columns and remove the -1s oops
        test_cols = []
        test_labels = []
        test_distributions = 3 if scaling_test else 4
        
        for i, col in enumerate(df.iloc[0]):
            if key in col:
                test_cols.append(df.columns[i])
                if not scaling_test:
                    # grab experiment 1 columns name
                    label = col.split(key+"_")[1].split(".csv")[0]
                    label = 'baseline' if '10users' in label else label
                    test_labels.append(label)
                if scaling_test:
                    # grab experiment 2 columns name
                    label = SCALING_TESTS.get(col.split("_")[2])
                    label = 'baseline' if '1 Instance' in label else label
                    test_labels.append(label) 

        # Perform ANOVA on auth columns
        data_list = [df[col].dropna()[1:].astype(float) for col in test_cols]
        df_data = pd.DataFrame(data_list).T
        df_data = df_data.fillna(df_data.mean())
        df_data.columns = test_labels

        num_bins = int(np.sqrt(len(df_data['baseline'])))
        for col in df_data.columns:
            df_data[col + '_bin'] = pd.cut(df_data[col], bins=num_bins, labels=False)

        # Save the binned data for the baseline
        baseline = df_data['baseline_bin']
        results = []

        # Loop through the distributions (hard coded to work for both)
        for column in df_data.columns[1:test_distributions]:
            to_compare = df_data[column + '_bin']
            contingency_table = pd.crosstab(baseline, to_compare)
            stat, p, _, _ = chi2_contingency(contingency_table)

            if p < 0.01:
                results.append(True)
            else:
                results.append(False)

        print("Chi Square Results (T=Significant Difference, F=No Difference):\n", results)

        # plot figures for final report
        figure_label= MICROSERVICE_TESTS.get(key)
        if scaling_test:
            figure_label += " Horizontal Scaling"
        generate_figures_for_test(data_list, test_labels, figure_label)


def main(args):
    exp1_df = load_data(args.experiment_1_file)
    exp2_df = load_data(args.experiment_2_file)

    # Perform ANOVA as statistical analysis
    perform_experiment_analysis(exp1_df)
    perform_experiment_analysis(exp2_df, scaling_test=True)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experiment-1-file", type=str,
    )
    parser.add_argument(
        "--experiment-2-file", type=str,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)
