import Utils from './utils';

class UserService {
    constructor() {
        this.axiosInstance = Utils.getAxiosInstance();
    }

    // Register a new user
    register(user) {
        return this.axiosInstance.post('/users/', user)
            .catch(error => {
                console.error('Registration error:', error);
                throw error;
            });
    }

    // Login user and store the token
    login(credentials) {
        return this.axiosInstance.post('/users/login/', credentials)
            .then(response => {
                if (response.data.token) {
                    Utils.setStorageItem('userToken', response.data.token);
                }
                return response.data;
            })
            .catch(error => {
                console.error('Login error:', error);
                throw error;
            });
    }

    // Get the profile
    getProfile() {
        return this.axiosInstance.get('/users/profile/')
            .catch(error => {
                console.error('Error fetching user profile:', error);
                throw error;
            });
    }

    // Update the profile
    updateProfile(user) {
        return this.axiosInstance.put('/users/profile/', user)
            .catch(error => {
                console.error('Error updating profile:', error);
                throw error;
            });
    }

    // Logout the user
    logout() {
        Utils.deleteStorageItem('userToken');
    }
}

export default new UserService();
