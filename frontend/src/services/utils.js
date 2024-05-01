import axios from 'axios';

class Utils {
    static API_URL = 'http://ec2-3-142-97-113.us-east-2.compute.amazonaws.com:8000/api';

    static getStorageItem(key) {
        return localStorage.getItem(key);
    }

    static setStorageItem(key, value) {
        localStorage.setItem(key, value);
    }

    static deleteStorageItem(key) {
        localStorage.removeItem(key);
    }

    static getAxiosInstance() {
        const axiosInstance = axios.create({
            baseURL: Utils.API_URL
        });

        axiosInstance.interceptors.request.use(config => {
            const token = Utils.getStorageItem('userToken');
            if (token) {
                config.headers['Authorization'] = `Token ${token}`;
            }
            return config;
        }, error => {
            return Promise.reject(error);
        });

        return axiosInstance;
    }

    static getExternalAxiosInstance() {
        return axios.create();
    }
}

export default Utils;
