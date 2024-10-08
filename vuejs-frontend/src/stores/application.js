import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

function checkJWT(token) {
    if (token === null || token === undefined) {
        return false;
    }
    const base64Url = token.split('.')[1];
    if (!base64Url) return false;
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Convert base64url to base64
    const payload = JSON.parse(atob(base64)); // Decode base64 and parse JSON
    const currentTime = Math.floor(Date.now() / 1000); // Get current time in Unix timestamp (seconds)
    return currentTime < payload.expires; // Check if token is expired
}
// function getUsernameFromToken(token) {
//     if (token === null || token === undefined) {
//         return false;
//     }
//     const base64Url = token.split('.')[1];
//     if (!base64Url) return false;
//     const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/'); // Convert base64url to base64
//     const payload = JSON.parse(atob(base64));
//     console.log("username data: ", payload);
//     return payload.user_id;
// }

export const useApplicationStore = defineStore('application', () => {
    const userData = ref(null);
    const tokenData = ref(null);

    const setUserData = (tempUserData) => {
        userData.value = tempUserData;
    };
    const setToken = (tempToken) => {
        tokenData.value = tempToken;
    };
    const persistUserData = () => {
        localStorage.setItem('userData', JSON.stringify(userData));
    };
    const persistToken = () => {
        localStorage.setItem('tokenData', JSON.stringify(tokenData.value));
    };
    const getUserData = () => {
        let tempUserData = localStorage.getItem('userData');
        tempUserData = JSON.parse(tempUserData);
        if (tempUserData === null || tempUserData === undefined) {
            return;
        }
        return tempUserData;
    };
    const getToken = () => {
        let token = localStorage.getItem('tokenData');
        token = JSON.parse(token);
        if (token === null || token === undefined) {
            return;
        }
        return token;
    };
    const loadUserData = () => {
        let tempUserData = localStorage.getItem('userData');
        tempUserData = JSON.parse(tempUserData);
        if (tempUserData === null || tempUserData === undefined) {
            return;
        }
        userData.value = tempUserData;
    };
    const loadTokenData = () => {
        let tempTokenData = localStorage.getItem('tokenData');
        tempTokenData = JSON.parse(tempTokenData);
        if (tempTokenData === null || tempTokenData === undefined) {
            return;
        }
        tokenData.value = tempTokenData;
    };
    const clearUserData = () => {
        localStorage.setItem('userData', JSON.stringify(null));
        userData.value = null;
    };
    const clearToken = () => {
        localStorage.setItem('tokenData', JSON.stringify(null));
        tokenData.value = null;
    };
    const isAuthenticated = computed(() => {
        // console.log("authendicated: ", tokenData.value?.access_token.access_token);
        return checkJWT(tokenData.value?.access_token.access_token);
    });

    return { userData, setUserData, persistUserData, persistToken, loadUserData, loadTokenData, clearUserData, clearToken, isAuthenticated, setToken, setUserData, getUserData, getToken };
});