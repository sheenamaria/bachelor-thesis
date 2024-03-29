from results.visualizations.plots.grouped_bar_plot_mean import GroupedBarPlotMean
from results.visualizations.plots.plot_utils import get_identifiers
from results.visualizations.plots.scatter_plot_mean_std import ScatterPlotMeanStd

CODE_DIFFERENCES = "Code Differences - Text Representation"


def scatter_plot_mean_and_std_diff_text_k_1_w_10_per_repo():
    title = CODE_DIFFERENCES
    plot_name = "scatter-plot-diff-text-mean-std-k-1-w-10"
    filter_criteria = {
        "term_strategy": "diff_text",
        "k": 1,
        "window_size": 10,
    }
    group_criteria = {
        "repository_identifier": get_identifiers(),
    }
    # red and grey
    colors = [
        "#E15759",
        "#818B91",
    ]
    scatter_plot = ScatterPlotMeanStd(
        title, plot_name, filter_criteria, group_criteria, colors=colors
    )
    scatter_plot.plot()


def grouped_bar_plot_mean_diff_text_by_k_per_repo():
    title = CODE_DIFFERENCES + "\n Mean Accuracy By Top-K per Repository"
    plot_name = "grouped-bar-plot-diff-text-by-k-per-repo"
    filter_criteria = {
        "term_strategy": "diff_text",
        "window_size": 10,
        "embeddings_concept": "tf_idf",
        "embeddings_strategy": "tf-idf-embedding--subword-tokenizer",
    }
    group_criteria = {
        "k": [1, 2, 3],
        "repository_identifier": get_identifiers(),
    }
    # blue, orange and red
    colors = [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
    ]
    grouped_bar_plot_mean = GroupedBarPlotMean(
        title,
        plot_name,
        filter_criteria,
        group_criteria,
        colors,
    )
    grouped_bar_plot_mean.plot()


def grouped_bar_plot_mean_diff_text_by_w_per_repo():
    title = CODE_DIFFERENCES + "\n Mean Accuracy By Window Size per Repository"
    plot_name = "grouped-bar-plot-diff-text-by-w-per-repo"
    filter_criteria = {
        "term_strategy": "diff_text",
        "k": 1,
        "embeddings_concept": "tf_idf",
        "embeddings_strategy": "tf-idf-embedding--subword-tokenizer",
    }
    group_criteria = {
        "window_size": [10, 20, 50],
        "repository_identifier": get_identifiers(),
    }
    # blue, orange and red
    colors = [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
    ]
    grouped_bar_plot_mean = GroupedBarPlotMean(
        title,
        plot_name,
        filter_criteria,
        group_criteria,
        colors,
    )
    grouped_bar_plot_mean.plot()


if __name__ == "__main__":
    scatter_plot_mean_and_std_diff_text_k_1_w_10_per_repo()
    grouped_bar_plot_mean_diff_text_by_k_per_repo()
    grouped_bar_plot_mean_diff_text_by_w_per_repo()
