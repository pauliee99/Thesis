<script setup>
import { RouterLink } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';
const applicationStore = useApplicationStore();

console.log("username: ", useApplicationStore.getUsername);
const rr = "qwe"

</script>

<template>
    <header class="text-bg-dark">
        <div class="container">
            <div class="d-flex flex-wrap justify-content-center py-2 px-3">
                <a
                    href="/"
                    class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none"
                >
                    <span class="fs-5 fw-bolder text-white">API Client</span>
                </a>
                <ul class="nav nav-pills">
                    <!-- @EXERCISE: Add different color to active link (improve UX/UX). -->
                    <!-- @EXERCISE: Add different color to active link with nested routes (improve UX/UX). -->
                    <!-- @EXERCISE: Hide links that users has no access to. -->
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'home' }" class="nav-link text-white"
                            >Home</router-link
                        >
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'students' }" class="nav-link text-white"
                            >Students</router-link
                        >
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === true">
                        <router-link :to="{ name: 'courses' }" class="nav-link text-white"
                            >Events</router-link
                        >
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === true">
                        <div class="profile-wrapper">
                            <div class="profile-circle">
                                <img src="/profile-default.png" alt="Profile Picture" class="profile-img">
                            </div>
                            <router-link :to="{ name: 'profile' }" class="nav-link text-white">
                                Profile</router-link>
                                <span style="font-size: 10px">
                                    ({{ rr }})
                                </span>
                        </div>
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === false">
                        <router-link :to="{ name: 'login' }" class="nav-link text-white"
                            >Login</router-link
                        >
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === false">
                        <router-link :to="{ name: 'register' }" class="nav-link text-white"
                            >Register</router-link
                        >
                    </li>
                    <li class="nav-item" v-if="applicationStore.isAuthenticated === true">
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
