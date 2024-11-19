from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import numpy as np
from scipy.stats import zscore
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Default dataset directory
DATASET_DIR = "./datasets"
ANALYSIS_DIR = "./analyses"

# Ensure required directories exist
os.makedirs(ANALYSIS_DIR, exist_ok=True)



def detect_anomalies(data, column, zscore_threshold, iqr_multiplier, stddev_multiplier):
    """
    Detect anomalies using Z-Score, IQR, and Mean-StdDev methods.
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    mean = data[column].mean()
    std_dev = data[column].std()

    anomalies = {
        "z_score": np.abs(zscore(data[column])) > zscore_threshold,
        "iqr": (data[column] < (Q1 - iqr_multiplier * IQR)) | (data[column] > (Q3 + iqr_multiplier * IQR)),
        "mean_stddev": (data[column] < (mean - stddev_multiplier * std_dev)) | (data[column] > (mean + stddev_multiplier * std_dev)),
    }

    return anomalies

def generate_interactive_plot(data, column, anomalies, feature_name, station_name):
    """
    Generate an interactive plot using Plotly with years on the x-axis and the feature name on the y-axis.
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    mean = data[column].mean()
    std_dev = data[column].std()

    # Ensure the index represents years
    x_values = data.index if data.index.name == "Year" else data.index.year

    # Base trace for the data
    traces = [
        go.Scatter(
            x=x_values,
            y=data[column],
            mode='lines',
            name='Values',
            line=dict(color='blue'),
        ),
        go.Scatter(
            x=x_values[anomalies["z_score"]],
            y=data[column][anomalies["z_score"]],
            mode='markers',
            name='Z-Score Anomalies',
            marker=dict(color='red', size=8),
        ),
        go.Scatter(
            x=x_values[anomalies["iqr"]],
            y=data[column][anomalies["iqr"]],
            mode='markers',
            name='IQR Anomalies',
            marker=dict(color='orange', size=8),
        ),
        go.Scatter(
            x=x_values[anomalies["mean_stddev"]],
            y=data[column][anomalies["mean_stddev"]],
            mode='markers',
            name='Mean-StdDev Anomalies',
            marker=dict(color='purple', size=8),
        ),
    ]

    # Add reference lines
    ref_lines = [
        go.Scatter(
            x=[x_values.min(), x_values.max()],
            y=[Q1, Q1],
            mode='lines',
            line=dict(dash='dot', color='green'),
            name='Q1 (IQR)',
        ),
        go.Scatter(
            x=[x_values.min(), x_values.max()],
            y=[Q3, Q3],
            mode='lines',
            line=dict(dash='dot', color='green'),
            name='Q3 (IQR)',
        ),
        go.Scatter(
            x=[x_values.min(), x_values.max()],
            y=[mean, mean],
            mode='lines',
            line=dict(color='purple'),
            name='Mean',
        ),
        go.Scatter(
            x=[x_values.min(), x_values.max()],
            y=[mean + 3 * std_dev, mean + 3 * std_dev],
            mode='lines',
            line=dict(dash='dot', color='red'),
            name='+3 Std Dev',
        ),
        go.Scatter(
            x=[x_values.min(), x_values.max()],
            y=[mean - 3 * std_dev, mean - 3 * std_dev],
            mode='lines',
            line=dict(dash='dot', color='red'),
            name='-3 Std Dev',
        ),
    ]

    # Combine traces and reference lines
    traces.extend(ref_lines)

    layout = go.Layout(
        title=dict(
            text=f'Station {station_name} - {feature_name} vs. Year',
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(title='Year'),
        yaxis=dict(title=feature_name),  # Use the feature name instead of ID
        legend=dict(orientation="h"),
        height=600,  # Adjust the height of the graph
    )

    return go.Figure(data=traces, layout=layout)


@app.route("/")
def index():
    return render_template("index.html")

def save_analysis_results(data, anomalies, column, station_id, feature_id):
    """
    Save the analysis results to an Excel file in the analysis folder.
    """
    result_df = data.copy()
    for key, mask in anomalies.items():
        result_df[f"{key}_anomalies"] = mask

    file_name = f"anomalies_{station_id}_{feature_id}_{column}.xlsx"
    file_path = os.path.join(ANALYSIS_DIR, file_name)
    result_df.to_excel(file_path, index=False)
    return file_path


@app.route("/analyze_single", methods=["POST"])
def analyze_single():
    """
    Analyze a single dataset and return the interactive plot data and a static download URL for the analysis file.
    """
    try:
        station_id = request.form.get("station_id")
        station_name = request.form.get("station_name", "Unknown")
        feature_id = request.form.get("feature_id")
        feature_name = request.form.get("feature_name", "Unknown Feature")  # Retrieve the feature name
        column = request.form.get("column")
        zscore_threshold = float(request.form.get("zscore_threshold", 3))
        iqr_multiplier = float(request.form.get("iqr_multiplier", 1.5))
        stddev_multiplier = float(request.form.get("stddev_multiplier", 3))

        if not station_id or not feature_id or not column:
            return jsonify({"error": "Station ID, Feature ID, and Column are required"}), 400

        # Locate the dataset
        station_folder = os.path.join(DATASET_DIR, station_id)
        file_name = f"weather_data_{station_id}_{feature_id}.xlsx"
        file_path = os.path.join(station_folder, file_name)

        if not os.path.exists(file_path):
            return jsonify({"error": f"Dataset not found: {file_name}"}), 404

        # Load the dataset
        df = pd.read_excel(file_path)
        if column not in df.columns:
            return jsonify({"error": f"Column {column} not found in dataset"}), 400

        # Ensure the 'Year' column is used as the index if available
        if "Year" in df.columns:
            df.set_index("Year", inplace=True)

        # Detect anomalies
        anomalies = detect_anomalies(df, column, zscore_threshold, iqr_multiplier, stddev_multiplier)

        # Save analysis results in the static/analyses directory
        # Format the station and feature names for file naming (replace spaces with underscores)
        station_name_safe = station_name.replace(" ", "_")
        feature_name_safe = feature_name.replace(" ", "_")

        # Generate the new file name
        analysis_file_name = f"anomalies_{station_name_safe}_{feature_name_safe}_{column}.xlsx"

        analysis_file_path = os.path.join("./static/analyses", analysis_file_name)
        os.makedirs("./static/analyses", exist_ok=True)  # Ensure the directory exists

        result_df = df.copy()
        for key, mask in anomalies.items():
            result_df[f"{key}_anomalies"] = mask

        result_df.to_excel(analysis_file_path, index=True)

        df.attrs["station_name"] = station_name  # Add the station name to the DataFrame attributes

        # Generate the interactive plot with the feature name
        fig = generate_interactive_plot(df, column, anomalies, feature_name, station_name)

        # Return both the Plotly JSON data and a static URL for the analysis file
        response = json.loads(fig.to_json())
        response["analysis_file_url"] = f"/static/analyses/{analysis_file_name}"
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=80, debug=True)
