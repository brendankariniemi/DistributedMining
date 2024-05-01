import Utils from './utils';

class RewardService {
    constructor() {
        this.axiosInstance = Utils.getAxiosInstance();
    }

    // Get the users reward info
    getRewards() {
        return this.axiosInstance.get('/mining/rewards/')
            .catch(error => {
                console.error('Error fetching user rewards:', error);
                throw error;
            });
    }
}

export default new RewardService();
