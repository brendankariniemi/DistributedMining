import Utils from "./utils";

class ResourceService {
    constructor() {
        this.axiosInstance = Utils.getAxiosInstance();
    }

    // Get the list of cryptocurrencies
    getCryptocurrencies() {

        return this.axiosInstance.get('/resources/cryptocurrencies').catch(error => {
            console.error('Error fetching cryptocurrencies:', error);
            throw error;
        });
    }

    // Get the list of guides
    getGuides() {
        return this.axiosInstance.get('/resources/guides').catch(error => {
            console.error('Error fetching guides:', error);
            throw error;
        });
    }

    // Get the list of tutorials
    getTutorial() {
        return this.axiosInstance.get('/resources/tutorials').catch(error => {
            console.error('Error fetching tutorials:', error);
            throw error;
        });
    }
}

export default new ResourceService();
