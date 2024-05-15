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
            return response.json();
        })
        .then(data => {
            setUserData(data);
            persistUserData();
            console.log("redirecting...");
            router.push({ name: 'profile' });
            
        })
        .catch((err) => {
            console.warn(err);
            passwordMismatch.value = true;
        })
        .finally(() => {
            loading.value = false;
        });
};


</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container-main">
            <br>
            <div class="old-password">
                <p id="old-psswd-txt">Current Password:</p>
                <input id="old-psswd-input" class="paswd-input" type="password">
            </div>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <div class="new-password">
                <p id="new-psswd-txt">New Password:</p>
                <input id="new-psswd-input" class="paswd-input" type="password">
            </div>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <div class="repeat-password">
                <p id="repeat-psswd-txt">Repeat Password:</p>
                <input id="repeat-psswd-input" class="paswd-input" type="password">
            </div>
            <br>
            <br>
            <br>
        </div>
    </div>
</template>
<style src="../assets/newpassword.css"></style>