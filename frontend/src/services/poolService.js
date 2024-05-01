import Utils from './utils';

class PoolService {
    constructor() {
        this.axiosInstance = Utils.getAxiosInstance();
        this.externalAxiosInstance = Utils.getExternalAxiosInstance();
    }

    // Register a new hardware client
    registerHardware(hardware) {
        return this.axiosInstance.post('/mining/hardware/', hardware)
            .catch(error => {
                console.error('Registration error:', error);
                throw error;
            });
    }

    // Get the pools
    getPools() {
        return this.axiosInstance.get('/mining/pools/')
            .catch(error => {
                console.error('Error fetching pools:', error);
                throw error;
            });
    }

    // Get pricing data for a specific cryptocurrency over the last 30 days
    getPricingData(crypto) {
        crypto = crypto.toLowerCase();
        const url = `https://api.coingecko.com/api/v3/coins/${crypto}/market_chart?vs_currency=usd&days=30`;
        return this.externalAxiosInstance.get(url)
            .then(response => response.data.prices)
            .catch(error => {
                console.error(`Failed to fetch pricing data for crypto ID ${crypto}:`, error);
                throw error;
            });
    }
}

export default new PoolService();
