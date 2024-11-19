# Weather Analysis Tool - Japan

## Overview
The **Weather Analysis Tool** allows users to analyze historical weather data from meteorological stations across Japan. It helps detect anomalies in weather trends using robust statistical methods and provides downloadable analysis reports.

---

## Features
### Input Options
- **Station Name**: Select a weather station (e.g., "ABASHIRI").
- **Feature**: Choose a weather parameter such as "Monthly mean vapor pressure."
- **Month**: Select a specific month for analysis (e.g., September).

### Statistical Parameters
- **Z-Score Threshold**: Detects anomalies based on how far data points deviate from the mean in terms of standard deviations.
- **IQR Multiplier**: Identifies outliers by analyzing the interquartile range of the dataset.
- **Mean-StdDev Multiplier**: Flags data points that fall outside a defined range of mean ± k × standard deviation.

### Outputs
- **Time-Series Graph**: Displays trends and anomalies across years for the selected station and parameter.
- **Anomalies Marked**:
  - Z-Score Anomalies: Extreme deviations based on standard deviations.
  - IQR Anomalies: Outliers outside interquartile bounds.
  - Mean-StdDev Anomalies: Data points outside a custom mean ± deviation range.
- **Downloadable Analysis**: Export results in a file format for further use.

---

## How It Works
### Anomaly Detection Methods
#### 1. Z-Score Method
- **Definition**: Flags data points that deviate significantly from the mean in terms of standard deviations.
- **Formula**:  
  Z = (X - μ) / σ  
  Where:
  - X = data point
  - μ = mean
  - σ = standard deviation
- **Custom Parameter**: 
  - **Z-Score Threshold**: This is the value the user sets (e.g., 3). It determines how many standard deviations away from the mean a data point must be to be considered an anomaly.
  - **Effect**: 
    - Lowering the threshold (e.g., 2) will make the detection more sensitive, flagging more anomalies.
    - Raising the threshold (e.g., 4) will make the detection stricter, flagging fewer anomalies.

---

#### 2. IQR Method
- **Definition**: Identifies outliers based on the interquartile range (IQR).
- **Formula**:  
  IQR = Q3 - Q1  
  - **Lower Bound**: Q1 - (1.5 × IQR)  
  - **Upper Bound**: Q3 + (1.5 × IQR)  
  Points outside this range are flagged as anomalies.
- **Custom Parameter**: 
  - **IQR Multiplier**: This is the value the user sets (e.g., 1.5). It determines how far outside the interquartile range (IQR) a point must be to be considered an anomaly.
  - **Effect**:
    - Lowering the multiplier (e.g., 1) will detect more anomalies by tightening the range.
    - Increasing the multiplier (e.g., 2) will loosen the range, reducing the number of flagged anomalies.

---

#### 3. Mean-StdDev Method
- **Definition**: Flags data points outside a specified range of the mean.
- **Formula**:  
  Anomaly Range = μ ± (k × σ)  
  Where:
  - k = user-defined multiplier
  - μ = mean
  - σ = standard deviation
- **Custom Parameter**: 
  - **Mean-StdDev Multiplier (k)**: This is the value the user sets (e.g., 3). It determines the number of standard deviations from the mean used to define the anomaly range.
  - **Effect**:
    - Lowering the multiplier (e.g., 2) will detect more anomalies by narrowing the acceptable range.
    - Raising the multiplier (e.g., 4) will reduce the number of flagged anomalies by broadening the acceptable range.

---

### Summary of Custom Parameters
1. **Z-Score Threshold**: Adjusts the sensitivity of anomaly detection based on standard deviations.
2. **IQR Multiplier**: Controls the range width for detecting outliers using the interquartile method.
3. **Mean-StdDev Multiplier**: Sets the tolerance level for anomalies based on the mean and standard deviation.

By adjusting these parameters, users can tailor the anomaly detection to the specific characteristics of their dataset or analysis goals.

---

## Getting Started
1. **Select Input Options**:
   - Choose a station, feature, and month for analysis.
2. **Adjust Parameters**:
   - Customize Z-Score, IQR, and Mean-StdDev multipliers as needed.
3. **Run the Analysis**:
   - Click “Analyze Dataset” to generate results.
4. **Download Results**:
   - Save the analysis as a downloadable report.

---

## Troubleshooting
- **No Anomalies Detected**: Lower the Z-Score or adjust the IQR multiplier for more sensitivity.
- **Graph Not Displaying**: Ensure all input fields are filled.
- **Export Fails**: Verify internet connection and storage space.

---

## Data Source
The tool uses historical weather data from the **Japan Meteorological Agency**:
[https://www.data.jma.go.jp/obd/stats/data/en/smp/index.html](https://www.data.jma.go.jp/obd/stats/data/en/smp/index.html)
