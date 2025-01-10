import https from 'https';

const getCurrencyCode = (currency) => {
    const currencyMapping = {
        "USD": 840,
        "UAH": 980,
        "EUR": 978,
        "GBP": 826,
        "JPY": 392,
        // Add more currency codes as needed
    };

    if (currency in currencyMapping) {
        return currencyMapping[currency];
    } else {
        throw new Error(`Currency code '${currency}' is not supported.`);
    }
};

const getCurrencyRate = (currencyFrom, currencyTo, rateType, jsonData) => {
    const currencyFromNum = getCurrencyCode(currencyFrom);
    const currencyToNum = getCurrencyCode(currencyTo);

    for (const item of jsonData) {
        if (item.currencyCodeA === currencyFromNum && item.currencyCodeB === currencyToNum) {
            if (item[rateType] !== undefined) {
                return item[rateType];
            } else {
                throw new Error(`Rate type '${rateType}' not found in the provided data.`);
            }
        }
    }

    throw new Error("The requested currency pair is not available in the provided data.");
};

export const handler = async (event) => {
    const options = {
        hostname: 'api.monobank.ua',
        path: '/bank/currency',
        method: 'GET',
    };

    const currencyFrom = "USD";
    const currencyTo = "UAH";
    const rateType = "rateBuy";

    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const jsonData = JSON.parse(data);

                    const rate = getCurrencyRate(currencyFrom, currencyTo, rateType, jsonData);
                    console.log(`The rate for ${currencyFrom}/${currencyTo} (${rateType}) is: ${rate}`);

                    resolve({
                        statusCode: 200,
                        body: JSON.stringify({
                            fromCurrency: currencyFrom,
                            toCurrency: currencyTo,
                            rate: rate
                        }),
                    });
                } catch (error) {
                    console.error('Error parsing data or retrieving rate:', error);
                    resolve({
                        statusCode: 500,
                        body: JSON.stringify({ message: 'Internal Server Error', error: error.message }),
                    });
                }
            });
        });

        req.on('error', (error) => {
            console.error('Error making API request:', error);
            resolve({
                statusCode: 500,
                body: JSON.stringify({ message: 'Internal Server Error' }),
            });
        });

        req.end();
    });
};
