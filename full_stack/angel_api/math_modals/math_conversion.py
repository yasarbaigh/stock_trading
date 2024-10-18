def candle_to_heikin_ashi(df):
    heikin_ashi_df = df.copy()

    heikin_ashi_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    # Initialize the first Heikin Ashi Open value as the original Open value
    heikin_ashi_df['HA_Open'] = 0.0
    heikin_ashi_df.loc[0, 'HA_Open'] = (df.loc[0, 'Open'] + df.loc[0, 'Close']) / 2

    # Calculate the rest of the Heikin Ashi Open values
    for i in range(1, len(df)):
        heikin_ashi_df.loc[i, 'HA_Open'] = (heikin_ashi_df.loc[i - 1, 'HA_Open'] + heikin_ashi_df.loc[
            i - 1, 'HA_Close']) / 2

    heikin_ashi_df['HA_High'] = heikin_ashi_df[['HA_Open', 'HA_Close', 'High']].max(axis=1)
    heikin_ashi_df['HA_Low'] = heikin_ashi_df[['HA_Open', 'HA_Close', 'Low']].min(axis=1)

    return heikin_ashi_df[['Date', 'HA_Open', 'HA_High', 'HA_Low', 'HA_Close']]