import pandas as pd
import warnings
warnings.simplefilter(action='ignore')


def make_Dataframe(data):
    # f = open(data, 'r', encoding="utf-8")
    # data = f.read()
    df = pd.DataFrame({'timeline': data.split('\n')})
    # df = pd.DataFrame({'timeline': [data]})
    df.drop(0, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df['date'] = df['timeline'].str.split(',').str[0]
    df['time'] = df['timeline'].str.split(',').str[1].str.split('-').str[0]
    df['user'] = df['timeline'].str.split(',').str[1].str.split('-').str[1].str.split(':').str[0]
    df['message'] = df['timeline'].str.split(',').str[1].str.split('-').str[1].str.split(':', 1).str[1]
    df['message_chars'] = df['message'].apply(lambda x: len(str(x)))
    df.dropna(inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.month_name()
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['minute'] = df['time'].str.split(':').str[1].str.split().str[0].astype(int)
    # df['date'] = df['date'].apply(lambda x: pd.Series([pd.Timestamp(x)]).dt.round('D'))

    def hour24(x):
        a = x.split(':')
        if 'PM' in a[1]:
            return int(a[0]) + 12
        else:
            return int(a[0])

    df['hour'] = df['time'].apply(hour24)
    df = df[['date', 'year', 'month', 'day', 'hour', 'minute', 'month_name', 'day_name', 'user', 'message',
             'message_chars']]

    return df
