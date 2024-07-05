<script setup>
import { ref, computed, watch  } from 'vue';
import { RouterLink } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';
const applicationStore = useApplicationStore();
console.log(applicationStore);
const { getUserData } = useApplicationStore();
// const { userData } = useApplicationStore();
// const { persistUserData, isAuthenticated, setToken, persistToken, setUserData } = useApplicationStore();
const URL_DEFAULT = "http://127.0.0.1:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null"
const tmp = getUserData();
// console.log("username blah: ", useApplicationStore.userData.username);
const username = ref('');
const role = ref('');
const url = ref('');

console.log(getUserData()?._value);

const userData = computed(() => applicationStore.userData);

watch(userData, (newValue) => {
  username.value = newValue?.username || '';
  role.value = newValue?.role || '';
  url.value = newValue?.profile_picture || '';
});
// const username = getUserData()?._value.username; //userData.
// const role = getUserData()?._value.role;
// const url = getUserData()?._value.profile_picture;
// console.log(url);
</script>

<template>
    <header class="text-bg-dark">
        <div class="container">
            <div class="d-flex flex-wrap justify-content-center py-2 px-3">
                <a
                    href="/"
                    class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none"
                >
                    <span class="fs-5 fw-bolder text-white">Erasmus Events</span>
                </a>
                <ul class="nav nav-pills">
                    <!-- @EXERCISE: Add different color to active link (improve UX/UX). -->
                    <!-- @EXERCISE: Add different color to active link with nested routes (improve UX/UX). -->
                    <!-- @EXERCISE: Hide links that users has no access to. -->
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'home' }" class="nav-link text-white"
                            >Home</router-link
                        >
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true && role === 'Admin'">
                        <router-link :to="{ name: 'students' }" class="nav-link text-white"
                            >Students</router-link
                        >
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'events' }" class="nav-link text-white"
                            >Events</router-link
                        >
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true" id="profile-stuff">
                        <div class="profile-wrapper-h">
   
                            <router-link :to="{ name: 'profile' }" class="nav-link text-white" style="display:flex; align-items: center;">
                                <div class="profile-circle-h">
                                    <!-- <img src="/profile-default.png" alt="Profile Picture" class="profile-img"> -->
                                    <img v-if="url" :src="url" class="profile-img-h">
                                    <img v-else :src="URL_DEFAULT" class="profile-img-h">
                                </div> 
                                Profile ({{ username }})</router-link>
                        </div>
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === false">
                        <router-link :to="{ name: 'login' }" class="nav-link text-white"
                            >Login</router-link
                        >
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === false">
                        <router-link :to="{ name: 'register' }" class="nav-link text-white"
                            >Register</router-link
                        >
                    </li>
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'logout' }" class="nav-link text-white"
                            >Logout</router-link
                        >
                    </li>
                </ul>
            </div>
        </div>
    </header>
</template>
<style src="../assets/header.css"></style>
