<script setup>
// @EXERCISE: If user is authenticated redirect to the requested URL.
// @EXERCISE: If user is not authenticated, keep the requested URL and after a successful authentication redirect to the requested resource.
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';

const router = useRouter();
const { setUserData, persistUserData, isAuthenticated, setToken, getToken, getRole } = useApplicationStore();

const loading = ref(false);
const credentials = ref({
    username: '',
<<<<<<< HEAD
    password: '',
});
const passwordMismatch = ref(false);

const password = ref(null);
const repeatPassword = ref(null);
const fname = ref(null);
const lname = ref(null);
const username = ref(null);
const birthdate = ref(null);
const studentid = ref(null);

const onFormSubmit = () => {
    loading.value = true;
    passwordMismatch.value = false;

    console.log('username: ', credentials.value.username, '  password: ', credentials.value.password);

    if (credentials.value.password !== repeatPassword.value) {
        console.error('Passwords do not match');
        passwordMismatch.value = true;
        return;
    }
    console.log('Passwords match');

    const requestBody = {
        id: 0,
        username: username.value,
        email: credentials.value.username,
        password: credentials.value.password,
        firstname: fname.value,
        lastname: lname.value,
        birth_date: birthdate.value,
        student_id: studentid.value,
        profile_picture: '',
        createdon: '2024-03-01T19:28:09',
        role: 'Student',
        disabled: false
    };
    console.log(requestBody);
=======
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
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
    fetch('http://localhost:8000/users/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to login');
            }
<<<<<<< HEAD
            return response.json();
=======
            // setUserData(response);
            // persistUserData();
            return response.json(); // Parse the response body as JSON
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
        })
        .then(data => {
            setUserData(data);
            persistUserData();
<<<<<<< HEAD
            console.log("redirecting...");
            router.push({ name: 'profile' });
=======
            // Handle successful login
            // Store authentication token in Vuex store or local storage
            // setToken(data.access_token);
            // Redirect to the dashboard or desired route
            console.log("redirecting...");
            if (getRole(data.access_token.access_token) == "Student"){
                router.push({ name: 'home' });
            } else if (getRole(data.access_token.access_token) == "Admin") {
                console.log("view for admin here");
            } else {
                console.log("view for manager here");
            }
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
            
        })
        .catch((err) => {
            console.warn(err);
<<<<<<< HEAD
            passwordMismatch.value = true;
=======
            authenticationFailed.value = true;
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
        })
        .finally(() => {
            loading.value = false;
        });
};

onBeforeMount(() => {
    if (isAuthenticated === true) {
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
                        <h1 class="fs-3">Register</h1>
                    </div>
                    <div class="spinner-border" role="status" v-if="loading">
                        <span class="visually-hidden">Loading...</span>
                    </div>
<<<<<<< HEAD
                    <form v-else @submit.prevent="onFormSubmit">
                        <div class="mb-2" v-if="passwordMismatch">
                            <div class="alert alert-danger" role="alert">
                                Passwords mismatch!
                            </div>
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="fanameFormControl" class="form-label mb-1"
                                >First Name</label
                            >
                            <input
                                v-model="fname"
                                type="text"
                                class="form-control"
                                id="fnameFormControl"
                            />
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="lanameFormControl" class="form-label mb-1"
                                >Last Name</label
                            >
                            <input
                                v-model="lname"
                                type="text"
                                class="form-control"
                                id="lnameFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="usernameFormControl" class="form-label mb-1"
                                >Email address</label
=======
                    <form v-else>
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
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
                            >
                            <input
                                v-model="credentials.username"
                                type="text"
                                class="form-control"
<<<<<<< HEAD
                                id="emailFormControl"
                            />
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="usernameFormControl" class="form-label mb-1"
                                >Username</label
                            >
                            <input
                                v-model="username"
                                type="text"
                                class="form-control"
=======
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
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
                        <div class="mb-2">
<<<<<<< HEAD
                            <label for="repeatPasswordFormControl" class="form-label mb-1"
                                >Repeat Password</label
                            >
                            <input
                                v-model="repeatPassword"
                                type="password"
                                class="form-control"
                                id="repeatPasswordFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="birthdateFormControl" class="form-label mb-1"
                                >Birth Date</label
                            >
                            <input
                                v-model="birthdate"
                                type="date"
                                class="form-control"
                                id="birthdateFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="studentidFormControl" class="form-label mb-1"
                                >Student ID</label
                            >
                            <input
                                v-model="studentid"
                                type="number"
                                class="form-control"
                                id="studentidFormControl"
=======
                            <label for="passwordFormControl" class="form-label mb-1"
                                >Repeat Password</label
                            >
                            <input
                                v-model="credentials.password"
                                type="password"
                                class="form-control"
                                id="passwordFormControl"
>>>>>>> 4fc18c6656d62d98e4d2db52a1e91b97762c81d9
                            />
                        </div>
                        <button @click="onFormSubmit" type="submit" class="btn btn-primary">
                            Register
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
