<script setup>
// @EXERCISE: If user is authenticated redirect to the requested URL.
// @EXERCISE: If user is not authenticated, keep the requested URL and after a successful authentication redirect to the requested resource.
import { onBeforeMount, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';

const router = useRouter();
const { persistUserData, isAuthenticated, setToken, persistToken, setUserData, loadUserData } = useApplicationStore();

const loading = ref(false);
const credentials = ref({
    username: '',
    password: ''
});
const authenticationFailed = ref(false);

const onFormSubmit = () => {
    loading.value = true;
    authenticationFailed.value = false;

    const requestBody = {
        email: credentials.value.username,
        password: credentials.value.password
    };
    fetch('http://localhost:8000/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => {
            // console.log(response);
            if (!response.ok) {
                throw new Error('Failed to login');
            }
            // setUserData(response);
            // persistUserData();
            return response.json(); // Parse the response body as JSON
        })
        .then(data => {
            setToken(data);
            persistToken();
            // Handle successful login
            // Store authentication token in Vuex store or local storage
            return fetch('http://localhost:8000/users/me', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${data.access_token.access_token}` // Assuming the access token is returned in the login response
                },
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user role');
            }
            return response.json(); // Parse the response body as JSON
        })
        .then(userData => {
            // Handle successful role fetch
            setUserData(userData);
            persistUserData();
            // Redirect based on user role
            if (userData.role === 'Student') {
                router.push({ name: 'home' });
            } else if (userData.role === "Admin") {
                router.push({ name: 'home' });
            } else {
                router.push({ name: 'home-manager' });
            }
        })
        .catch((err) => {
            console.warn(err);
            authenticationFailed.value = true;
        })
        .finally(() => {
            loading.value = false;
        });
};

onBeforeMount(() => {
    if (isAuthenticated === true) {
        loadUserData();
        router.push({ name: 'home' });
    }
});
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-4">
                    <div class="mb-4">
                        <h1 class="fs-3">Login</h1>
                    </div>
                    <div class="spinner-border" role="status" v-if="loading">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <form @submit.prevent="onFormSubmit" v-else>
                        <div class="mb-2" v-if="authenticationFailed">
                            <!--
              @EXERCISE: Be more specific.
              E.g., user does not exist, credentials are not valid, etc.
              Always consider security, i.e., sometimes you may not want to unveil information.
              -->
                            <div class="alert alert-danger" role="alert">
                                Authentication failed!
                            </div>
                        </div>
                        <div class="mb-2">
                            <label for="usernameFormControl" class="form-label mb-1"
                                >Email address or Username</label
                            >
                            <input
                                v-model="credentials.username"
                                type="text"
                                class="form-control"
                                id="usernameFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="passwordFormControl" class="form-label mb-1"
                                >Password</label
                            >
                            <input
                                v-model="credentials.password"
                                type="password"
                                class="form-control"
                                id="passwordFormControl"
                            />
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Login
                            <span class="fst-italic" v-if="credentials.username"
                                >as {{ credentials.username }}</span
                            >
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
