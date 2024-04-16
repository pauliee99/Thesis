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
                            <img v-if="userData.picture === undefined" src="http://192.168.2.9:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null" alt="Profile Picture" class="profile-img">
                            <img v-else :src="userData.profile_picture" alt="Profile Picture" class="profile-img">
                            <img id="edit-profilepicture" class="profile-img" src="http://192.168.2.9:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=ZWRpdC1wcm9maWxlLXBpY3R1cmUuc3Zn&version_id=null"></img>
                        </div>
                        <!-- @EXERCISE: Create a nice component to present user data -->
                        <pre>{{ userData }}</pre>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style src="../assets/profile.css"></style>