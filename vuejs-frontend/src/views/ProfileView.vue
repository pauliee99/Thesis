<script setup>
import { useApplicationStore } from '@/stores/application.js';
const { userData } = useApplicationStore();


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
                            <img v-if="userData.picture === undefined" src="http://192.168.2.29:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null" alt="Profile Picture" class="profile-img">
                            <img v-else :src="userData.profile_picture" alt="Profile Picture" class="profile-img">
                            <img id="edit-profilepicture" class="profile-img" src="http://192.168.2.9:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=ZWRpdC1wcm9maWxlLXBpY3R1cmUuc3Zn&version_id=null"></img>
                        </div>
                        <!-- @EXERCISE: Create a nice component to present user data -->
                        <pre>{{ userData }}</pre>
                    </div>
                    <div class="container mb-4">
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="picture">Profile Picture</label>
                                <div class="setup-picture">
                                <!-- <h1 class='center light gray mt-15'>Start setting your account Picture</h1> -->
                                    <form method="post" onsubmit="return false">
                                        <img src='#' id='uploaded'> <!-- Uploaded picture goes here -->
                                        <div class="picture">
                                        <input type="file"  name="event_picture" id="event_picture" @change="previewPicture">
                                        <font-awesome-icon icon="camera" />
                                        <h3>Choose your picture</h3>
                                        <div class='clearfix'></div>
                                        </div>
                                        <button class='btn btn-dark mt-15'>Upload Picture</button>
                                    </form>
                                </div>
                            </div>
                            <div class="mb-2">
                                <label for="role">Select Role:</label>
                                <select class="form-control" id="role" :disabled="true">
                                    <option :value="userData.role" selected>{{ getRoleName(userData.role) }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="firstName">First Name</label>
                                <input class="form-control" id="firstName" v-model="userData.firstname" type="text" />
                            </div>
                            <div class="mb-2">
                                <label for="lastName">Last Name</label>
                                <input class="form-control" id="lastName" v-model="userData.lastname" type="text" />
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="email">Email</label>
                                <input class="form-control" id="email" v-model="userData.email" type="email" />
                            </div>
                            <div class="mb-2">
                                <label for="username">Username</label>
                                <input class="form-control" id="username" v-model="userData.username" type="text" />
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="password">Password</label>
                                <input class="form-control" id="password" v-model="userData.password" type="password" />
                            </div>
                        </div>
                        <div class="mb-parent">
                            <div class="mb-2">
                                <label for="studentid">Student Id</label>
                                <input class="form-control" id="student_id" v-model="userData.student_id" type="text" />
                            </div>
                            <div class="mb-2">
                                <label for="birthday">Birthday</label>
                                <input class="form-control" id="birth_date" v-model="userData.birth_date" type="date" />
                            </div>
                        </div>
                        <div class="">
                            <button class="btn btn-primary" @click="onSubmit" type="button">
                                Create new user
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style src="../assets/profile.css"></style>