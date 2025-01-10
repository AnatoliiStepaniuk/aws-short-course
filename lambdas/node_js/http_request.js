import https from 'https';

// https://api.monobank.ua/bank/currency

export const handler = async (event) => {
    const options = {
        hostname: 'api.monobank.ua',
        path: '/bank/currency',
        method: 'GET',
    };

    return new Promise((resolve, reject) => {
        const req = https.request(options, (res) => {
            let data = '';

            // Listen for data chunks
            res.on('data', (chunk) => {
                data += chunk;
            });

            // Response has ended
            res.on('end', () => {
                resolve({
                    statusCode: 200,
                    body: data,
                });
            });
        });

        // Handle request errors
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
