-- Table should be created from Frontend using flask-db and migrate!
CREATE TABLE IF NOT EXISTS quotes (
    symbol text,
    name text,
    price numeric,
    priceChange numeric,
    percentChange numeric,
    exchangeName text,
    exShortName text,
    exchangeCode text,
    marketPlace text,
    sector text,
    industry text,
    volume bigint,
    openPrice numeric,
    dayHigh numeric,
    dayLow numeric,
    MarketCap bigint,
    MarketCapAllClasses bigint,
    peRatio numeric,
    prevClose numeric,
    dividendFrequency text,
    dividendYield numeric,
    dividendAmount numeric,
    dividendCurrency text,
    beta numeric,
    eps numeric,
    exDividendDate timestamp,
    shortDescription text,
    longDescription text,
    website text,
    email text,
    phoneNumber text,
    fullAddress text,
    employees int,
    shareOutStanding bigint,
    totalDebtToEquity numeric,
    totalSharesOutStanding bigint,
    sharesESCROW bigint,
    vwap numeric,
    dividendPayDate timestamp,
    weeks52high numeric,
    weeks52low numeric,
    alpha numeric,
    averageVolume10D bigint,
    averageVolume30D bigint,
    averageVolume50D bigint,
    priceToBook numeric,
    priceToCashFlow numeric,
    returnOnEquity numeric,
    returnOnAssets numeric,
    day21MovingAvg numeric,
    day50MovingAvg numeric,
    day200MovingAvg numeric,
    dividend3Years numeric,
    dividend5Years numeric,
    datatype text,
    typename text,
    lastupdate timestamp,

    UNIQUE (symbol, name)
);

