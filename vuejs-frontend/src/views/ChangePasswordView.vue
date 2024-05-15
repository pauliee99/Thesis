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

};
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container-main">
            <br>
            <div class="old-password">
                <p id="old-psswd-txt-a32">Current Password:</p>
                <input id="old-psswd-input-a32" class="paswd-input" type="password">
            </div>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <div class="new-password">
                <p id="new-psswd-txt-a32">New Password:</p>
                <input id="new-psswd-input-a32" class="paswd-input" type="password">
            </div>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <span class="dot"></span>
            <br>
            <div class="repeat-password">
                <p id="repeat-psswd-txt-a32">Repeat Password:</p>
                <input id="repeat-psswd-input-a32" class="paswd-input" type="password">
            </div>
            <br>
            <br>
            <button id="submit-a32">Submit</button>
            <br>
            <br>
        </div>
    </div>
</template>
<style src="../assets/newpassword.css"></style>