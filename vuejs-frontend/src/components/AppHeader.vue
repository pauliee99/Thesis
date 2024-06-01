<script setup>
import { ref, computed, watch  } from 'vue';
import { RouterLink } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';
const applicationStore = useApplicationStore();
const { getUserData } = useApplicationStore();
// const { userData } = useApplicationStore();
// const { persistUserData, isAuthenticated, setToken, persistToken, setUserData } = useApplicationStore();
const tmp = getUserData();
// console.log("username blah: ", useApplicationStore.userData.username);
const username = ref('');
const role = ref('');

console.log(getUserData()?._value);

const userData = computed(() => applicationStore.getUserData());

watch(userData, (newValue) => {
  username.value = newValue?.username || '';
  role.value = newValue?.role || '';
});
// const username = getUserData()?._value.username; //userData.
// const role = getUserData()?._value.role;
const url = getUserData()?._value.profile_picture;
console.log(url);
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
                    <li class="nav-item-h" v-if="applicationStore.isAuthenticated === true">
                        <div class="profile-wrapper-h">
                            <div class="profile-circle-h">
                                <!-- <img src="/profile-default.png" alt="Profile Picture" class="profile-img"> -->
                                <img :src="url" class="profile-img-h">
                            </div>
                            <router-link :to="{ name: 'profile' }" class="nav-link text-white">
                                Profile</router-link>
                                <span style="font-size: 10px">
                                    ({{ username }})
                                </span>
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
