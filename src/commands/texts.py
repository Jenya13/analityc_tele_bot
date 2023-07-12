start_message = 'Hi! {}\n' +\
    'This bot created to analyze assets or groups of assets\n' +\
    'Use /help command to review his functionality'


help_message = "/single_asset - Analyzes a single asset and outputs its statistics\n" +\
    "/assets_group - Analyzes a group of assets and outputs their statistics\n" +\
    "/asset_behavior - Analyzes a single asset trading behavior\n" +\
    "/terms - A brief explanation of a concepts"


terms_message = "<b>1. Drawdown:</b> Drawdown refers to the peak-to-trough decline during a specific period for an investment or trading strategy. It measures the percentage decline from the highest value to the lowest value in the investment's net asset value. Drawdown helps assess the risk and volatility of an investment and is used to evaluate the potential downside risk.\n\n" +\
    "<b>2. Sharpe Ratio:</b> The Sharpe Ratio is a measure of risk-adjusted return. It quantifies the excess return generated per unit of risk taken. It is calculated by subtracting the risk-free rate of return from the portfolio's average return and dividing it by the standard deviation of the portfolio's returns. The higher the Sharpe Ratio, the better the risk-adjusted performance.\n\n" +\
    "<b>3. Sortino Ratio:</b> The Sortino Ratio is another risk-adjusted return measure, similar to the Sharpe Ratio. However, it only considers the downside risk, focusing on the standard deviation of negative returns. It provides a measure of the return earned per unit of downside risk. A higher Sortino Ratio indicates better risk-adjusted performance in terms of minimizing downside volatility.\n\n" +\
    "<b>4. Alpha:</b> Alpha represents the excess return of an investment or portfolio compared to a benchmark. It measures the investment's performance independent of market movements. Positive alpha indicates outperformance, while negative alpha suggests underperformance relative to the benchmark. Alpha is used to assess the skill of an investment manager or trading strategy.\n\n" +\
    "<b>5. Beta:</b> Beta measures the sensitivity of an investment's returns to the overall market movements. It indicates how closely the investment's returns align with the benchmark's returns. A beta of 1 means the investment moves in line with the market, while a beta greater than 1 suggests higher volatility than the market, and a beta less than 1 indicates lower volatility.\n\n" +\
    "<b>6. Mean Log Returns:</b> Mean Log Returns refers to the average logarithmic return of an investment or trading strategy. Log returns are commonly used in finance because they provide additive properties and are more suitable for analyzing returns over longer periods. Mean Log Returns help assess the average performance of an investment or strategy.\n\n" +\
    "<b>7. Standard Deviation Log Returns:</b> Standard Deviation Log Returns measures the dispersion or volatility of logarithmic returns. It quantifies the degree of fluctuation or risk associated with an investment or trading strategy. A higher standard deviation indicates greater volatility, while a lower standard deviation suggests lower risk and stability.\n\n" +\
    "<b>8. Annualized Performance:</b> Annualized Performance refers to the compounded return of an investment or trading strategy over a year. It calculates the average annual return based on the investment's overall performance. Annualizing performance allows for better comparison and evaluation of investment returns over different time periods.\n\n" +\
    "<b>9. Skewness:</b> Skewness measures the asymmetry of the probability distribution of investment returns. It assesses whether the returns are skewed towards positive or negative values. Positive skewness indicates a longer tail towards higher returns, while negative skewness suggests a longer tail towards lower returns. Skewness helps understand the distribution characteristics and potential risks.\n\n" +\
    "<b>10. Kurtosis:</b> Kurtosis measures the shape of the probability distribution of investment returns. It assesses the presence of extreme values or outliers in the distribution. Higher kurtosis indicates a distribution with heavier tails and potentially more extreme returns, while lower kurtosis suggests a distribution with lighter tails and less extreme returns.\n\n" +\
    "These concepts are widely used in finance and trading to evaluate performance, risk, and statistical properties of investments or trading strategies. Understanding these concepts can help investors and traders make informed decisions and assess the potential risks and rewards associated with their investments.\n"


single_asset_analitics_text = 'Ticker:                                  {}\n' +\
    'Start Time:                          {}\n' +\
    'End Time:                            {}\n' +\
    '---------------------------------------------------------------\n' +\
    'Drawdown -                          {}%\n' +\
    'Sharp (risk-adjusted) -        {}\n' +\
    'Sortino -                                {}\n' +\
    'Alpha (excess return) -       {}%\n' +\
    'Beta (volatility) -                  {}\n' +\
    'Skew -                                   {}\n' +\
    'Kurtosis -                               {}\n' +\
    'Risk: {}% | Return: {}%\n'


single_asset_returns_text = 'Mean Returns -                    {}%\n' +\
    'STD Returns -                      {}%\n'
