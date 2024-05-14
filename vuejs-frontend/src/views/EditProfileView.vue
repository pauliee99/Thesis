<script setup>
import { useApplicationStore } from '@/stores/application.js';
import { ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
const { userData } = useApplicationStore();
const { getToken } = useApplicationStore();

const formDataRef = ref({
    firstname: userData.firstname,
    lastname: userData.lastname,
    email: userData.email,
    username: userData.username,
    birth_date: userData.birth_date,
    profile_picture: userData.profile_picture,
    student_id: userData.student_id,
    disabled: userData.disabled,
});

const token = getToken()?.access_token.access_token;

const userIdRef = ref(null);
const urlRef = computed(() => {
    return 'http://localhost:8000/users/' + userIdRef.value;
});
const authRef = ref(true);
const methodRef = ref('PUT');
const showpopup = ref(false);

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);

const onSubmit = () => {
    // formDataRef.value.createdon = "2024-02-22T00:00:00";
    // formDataRef.value.picture = null;    
    performRequest({ token });
};
const goBack = () => {
    window.history.back();
};
const changePassword = () => {
    console.log("password screen");
};
const onDeleteProfile = () => {
    console.log("delete profile");
};
// @TODO: prepi touto na gini sosta (thkiavazo ta data pou to userData prepi na ferno jenourka)
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3">Profile eee</h1>
                    </div>
                    <div>
                        <div class="profileviewcircle">
                            <img v-if="userData.picture === undefined" src="http://127.0.0.1:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null" alt="Profile Picture" class="profile-img">
                            <img v-else :src="userData.profile_picture" alt="Profile Picture" class="profile-img">
                            <img id="edit-profilepicture" class="profile-img" src="http://127.0.0.1:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=ZWRpdC1wcm9maWxlLXBpY3R1cmUuc3Zn&version_id=null">
                        </div>
                        <!-- <pre>{{ userData }}</pre> -->
                    </div>
                    <br>
                    <div class="container mb-4">
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="firstName">First Name</label>
                                <input class="form-control" id="firstName" v-model="userData.firstname" type="text" />
                            </div>
                            <div class="mb-2">
                                <label for="lastName">Last Name</label>
                                <input class="form-control" id="lastName" v-model="userData.lastname" type="text"/>
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="email">Email</label>
                                <input class="form-control" id="email" v-model="userData.email" type="email"/>
                            </div>
                            <div class="mb-2">
                                <label for="username">Username</label>
                                <input class="form-control" id="username" v-model="userData.username" type="text"/>
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="studentid">Student Id</label>
                                <input class="form-control" id="student_id" v-model="userData.student_id" type="text" v-if="userData.role ==='Student'"/>
                            </div>
                            <div class="mb-2">
                                <label for="birthday">Birthday</label>
                                <input class="form-control" id="birth_date" :value="userData.birth_date" type="date"/>
                            </div>
                            <!-- <div class="mb-2">
                                <label for="role">Select Role:</label>
                                <select class="form-control" id="role">
                                    <option :value="userData.role" selected>{{ userData.role }}</option>
                                </select>
                            </div> -->
                        </div>
                        <div class="" style="display: flex; justify-content: space-between;">
                            <button class="btn btn-primary" @click="goBack" type="button">
                                Cancel Changes
                            </button>
                            <button class="btn btn-primary" @click="onSubmit" type="button">
                                Save Changes
                            </button>
                        </div>
                        <br>
                        <div class="" style="display: flex; justify-content: space-between;">
                            <router-link :to="{ name: 'changepassword' }">
                                <button class="btn btn-primary" @click="changePassword" type="button">
                                    Change Password
                                </button>
                            </router-link>
                            <button class="btn btn-primary" @click="showpopup = true" type="button" id="delete-button">
                                Delete Profile
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="overlay" id="overlay" v-if="showpopup==true">
        <!-- Content inside the overlay -->
        <div class="content">
        <a href="#" class="close-button" @click="showpopup = false">&#10006;</a>
        <h2 style="text-align: center;">Delete Profile?</h2>
        <h3 style="text-align: center;">This Change cannot be undone. Do you really want to delete your profile?</h3>
        <div class="response-container">
            <button id="cancel-button" @click="showpopup = false">Cacnel</button>
            <button id="continue-button" @click="onDeleteProfile">Delete</button>
        </div>
        </div>
    </div>

</template>
<style src="../assets/profile.css"></style>