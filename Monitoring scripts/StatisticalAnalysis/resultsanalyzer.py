import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# for anova
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

EXPERIMENT_1_TESTS = {
    "auth": "Authentication",
    "webhvy": "WebUI Heavy Use",
    "weblgt": "WebUI Light Use",
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
    fig, axes = plt.subplots(len(data_list), 1, figsize=(8, 2 * len(data_list)))
    for i, data in enumerate(data_list):
        axes[i].hist(data, bins=num_bins)
        axes[i].set_title(f'Histogram for {figure_name} Distribution {data_labels[i]}')
        axes[i].set_xlabel('Values')
        axes[i].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(f"results_statistics/Histograms_{figure_name.replace(' ', '_')}.png")
    plt.close()

    return

def perform_anova_and_plot(df):
    for key in EXPERIMENT_1_TESTS:
        # Separate test columns and remove the -1s oops
        test_cols = []
        test_labels = []
        
        for i, col in enumerate(df.iloc[0]):
            if key in col:
                test_labels.append(col.split(key+"_")[1].split(".csv")[0])
                test_cols.append(df.columns[i])
    
        # Perform ANOVA on auth columns
        data_list = [df[col].dropna()[1:].astype(float) for col in test_cols]
        df_data = pd.DataFrame(data_list).T
        df_data = df_data.fillna(df_data.mean())
        df_data.columns = test_labels

        # Melt the DataFrame to long format for ols
        df_melted = df_data.melt(var_name='Group', value_name='Value')
        model = ols('Value ~ C(Group)', data=df_melted).fit()

        # Perform ANOVA
        anova_table = sm.stats.anova_lm(model, typ=2)
        p_value = anova_table.loc['C(Group)', 'PR(>F)']
        print("\n\nANOVA RESULTS")
        print(anova_table)
        print(p_value)
        if p_value < 0.05:
            print ("Distributions are statistically different... continuing to pairwise comparisons")

            # Compare each pair of response time distributions using a post hoc tukey test 
            tukey_results = pairwise_tukeyhsd(df_melted['Value'], df_melted['Group'])
            print("\n\nPAIRWISE DISTRIBUTION COMPARISONS")
            print(tukey_results)

        # plot figures for final report
        generate_figures_for_test(data_list, test_labels, EXPERIMENT_1_TESTS.get(key))

def compare_with_10users(auth_columns, p_values, df):
    # Compare with "10users" column
    ten_users_column = [col for col in df.columns if "10users" in col][0]
    significant_columns = []

    for col, p_value in zip(auth_columns, p_values):
        if p_value < 0.05:  # significance level
            if col != ten_users_column:
                significant_columns.append(col)

    return significant_columns

def main(args):
    df = load_data(args.combined_file)

    # Perform ANOVA as statistical analysis
    perform_anova_and_plot(df)

    # Compare with "10users" column
    # significant_columns = compare_with_10users(auth_columns, p_values, df)

    # print("Columns significantly different from '10users':", significant_columns)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--combined-file", type=str,
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main(args)
