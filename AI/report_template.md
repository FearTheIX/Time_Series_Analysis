# Laboratory Work 6 - Time Series Analysis Report

## 1. Dataset Overview
- **Source**: [Data source description]
- **Period**: [Start date] - [End date]
- **Records**: [Number of records]
- **Variables**: [List of variables]

## 2. Time Series Analysis

### 2.1 Stationarity
- ADF Test p-value: [value]
- KPSS Test p-value: [value] 
- Conclusion: [Stationary/Non-stationary]

### 2.2 Autocorrelation
- Significant ACF lags: [list]
- Significant PACF lags: [list]
- Seasonality detected: [Yes/No]

## 3. Model Performance

### 3.1 SARIMA Model
- Best parameters: [parameters]
- Evaluation metrics:
  - MSE: [value]
  - MAE: [value]
  - RMSE: [value]
  - MAPE: [value]

### 3.2 Regression Models
- Linear Regression metrics:
  - MSE: [value]
  - MAE: [value]
- Random Forest metrics:
  - MSE: [value]
  - MAE: [value]

## 4. Hyperparameter Tuning Results

### 4.1 SARIMA Tuning
| Parameters | AIC | Status |
|------------|-----|--------|
| [params1] | [aic1] | [status1] |
| [params2] | [aic2] | [status2] |

### 4.2 Random Forest Tuning
| n_estimators | max_depth | min_samples_split | MSE |
|--------------|-----------|-------------------|-----|
| [params1] | [value] | [value] | [mse1] |
| [params2] | [value] | [value] | [mse2] |

## 5. Best Model Selection
- **Selected model**: [Model name]
- **Reason**: [Justification]
- **Final metrics**: [Metrics]

## 6. Conclusion
[Summary of findings and recommendations]