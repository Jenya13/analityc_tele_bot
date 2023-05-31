start_message = 'Hi! {}\n' +\
    'This bot created to analyze assets or groups of assets\n' +\
    'Use /help command to review his functionality'


help_message = '/single_asset Analyzes a single asset and outputs its statistics\n' +\
    '/assets_group Analyzes a group of assets and outputs their statistics\n' +\
    '/behavior Analyzes a single asset trading behavior'


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
