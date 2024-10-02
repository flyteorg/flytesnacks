(time_series_modeling)=

# Time Series Modeling

```{eval-rst}
.. tags:: Advanced, MachineLearning
```

Time series data is fundamentally different from Independent and Identically
Distributed (IID) data, which is commonly used in many machine learning tasks.
Here are a few key differences:

1. **Temporal Dependency**: In time series data, observations are ordered
   chronologically and exhibit temporal dependencies. Each data point is related
   to its past and future values. This sequential nature is crucial for
   forecasting and trend analysis. In contrast, IID data assumes that each
   observation is independent of others.
2. **Non-stationarity**: Time series often display trends, seasonality, or cyclic
   patterns that evolve over time. This non-stationarity means that statistical
   properties like mean and variance can change, making analysis more complex. IID
   data, by definition, maintains constant statistical properties.
3. **Autocorrelation**: Time series data frequently shows autocorrelation, where
   an observation is correlated with its own past values. This feature is essential
   for many time series models but is not the case for IID data.
4. **Importance of Order**: The sequence of observations in time series data is
   critical and cannot be shuffled without losing information. In IID data, the
   order of observations is assumed to be irrelevant.
5. **Inference is Focused on Forecasting**: Time series analysis often aims to
   predict future values based on historical patterns, whereas many machine
   learning tasks with IID data focus on classification or regression without
   a temporal component.
6. **Specific Modeling Techniques**: Time series data requires specialized
   modeling techniques like ARIMA, Prophet, or RNNs that can capture temporal
   dynamics. These models are not typically used with IID data.

Understanding these differences is crucial for selecting appropriate analysis
methods and interpreting results in time series modeling tasks.

Below are examples demonstrating how to use Flyte to train time series models.

## Examples

```{auto-examples-toc}
neural_prophet
```
