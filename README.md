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
  \[
  Z = \frac{(X - \mu)}{\sigma}
  \]  
  Where \(X\) = data point, \(\mu\) = mean, \(\sigma\) = standard deviation.
- **Threshold**: Data points with \(|Z| > 3\) are anomalies.

#### 2. IQR Method
- **Definition**: Identifies outliers based on the interquartile range (IQR).
- **Formula**:  
  \[
  IQR = Q3 - Q1
  \]  
  - **Lower Bound**: \(Q1 - (1.5 \times IQR)\)  
  - **Upper Bound**: \(Q3 + (1.5 \times IQR)\)  
  Points outside this range are flagged as anomalies.

#### 3. Mean-StdDev Method
- **Definition**: Flags data points outside a specified range of the mean.
- **Formula**:  
  \[
  \text{Anomaly Range} = \mu \pm (k \times \sigma)
  \]  
  Where \(k\) = user-defined multiplier.

---

## Use Cases
- **Climate Change Research**: Detect long-term shifts in weather patterns.
- **Environmental Risk Assessment**: Identify extreme weather events or irregular trends.
- **Operational Planning**: Use historical data to inform agriculture, infrastructure, or tourism decisions.

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
