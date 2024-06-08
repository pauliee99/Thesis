<script setup>
// import { RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import { useApplicationStore } from '@/stores/application.js';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useRouter, useRoute } from 'vue-router';
const { persistUserData, setUserData } = useApplicationStore();

// const { userData } = useApplicationStore();

const { getToken } = useApplicationStore();
const token = getToken()?.access_token.access_token;

const userData = ref({});
const urlRef = ref('http://localhost:8000/users/me');
const authRef = ref(true);
const methodRef = ref('GET');
const formDataRef = ref(null);

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);

const fetchUserData = async () => {
    try {
        const response = await fetch('http://localhost:8000/users/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });
        if (response.ok) {
            // setUserData(response.data);
            // persistUserData();
            userData.value = await response.json();
        } else {
            console.error('Failed to fetch user data:', response);
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
};

onMounted(fetchUserData);
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3">Profile</h1>
                    </div>
                    <div>
                        <div class="profileviewcircle">
                            <img v-if="userData.profile_picture === undefined" src="http://127.0.0.1:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null" alt="Profile Picture" class="profile-img">
                            <img v-else :src="userData.profile_picture" alt="Profile Picture" class="profile-img">
                            <!-- <img id="edit-profilepicture" class="profile-img" src="http://127.0.0.1:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=ZWRpdC1wcm9maWxlLXBpY3R1cmUuc3Zn&version_id=null"></img> -->
                        </div>
                        <!-- <pre>{{ userData }}</pre> -->
                    </div>
                    <br>
                    <div class="container mb-4">
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="firstName">First Name</label>
                                <input class="form-control" id="firstName" v-model="userData.firstname" type="text" :disabled="true"/>
                            </div>
                            <div class="mb-2">
                                <label for="lastName">Last Name</label>
                                <input class="form-control" id="lastName" v-model="userData.lastname" type="text" :disabled="true"/>
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="email">Email</label>
                                <input class="form-control" id="email" v-model="userData.email" type="email" :disabled="true"/>
                            </div>
                            <div class="mb-2">
                                <label for="username">Username</label>
                                <input class="form-control" id="username" v-model="userData.username" type="text" :disabled="true"/>
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="studentid">Student Id</label>
                                <input class="form-control" id="student_id" v-model="userData.student_id" type="text" :disabled="true" v-if="userData.role ==='Student'"/>
                            </div>
                            <div class="mb-2" v-if="userData.birth_date">
                                <label for="birthday">Birthday</label>
                                <input class="form-control" id="birth_date" :value="userData.birth_date" type="date" :disabled="true"/>
                            </div>
                            <div class="mb-2">
                                <label for="role">Select Role:</label>
                                <select class="form-control" id="role" :disabled="true">
                                    <option :value="userData.role" selected>{{ userData.role }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="">
                            <RouterLink :to="{ name: 'editprofile' }">
                                <button class="btn btn-primary" @click="onSubmit" type="button">
                                    Edit Profile
                                </button>
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style src="../assets/profile.css"></style>