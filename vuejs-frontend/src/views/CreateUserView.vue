<script setup>
import { ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';

const formDataRef = ref({
    id: 0,
    firstname: '',
    lastname: '',
    email: '',
    username: '',
    password: '',
    birth_date: '',
    profile_picture: 'http://127.0.0.1:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null',
    student_id: null,
    role: null,
    createdon: '2024-05-04T15:58:19.765Z',
    disabled: false,
});
const urlRef = ref('http://localhost:8000/users/signup');
const authRef = ref(true);
const methodRef = ref('POST');

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);

const onSubmit = () => {
    console.log(formDataRef?._rawValue);
    performRequest(formDataRef?._rawValue);
};
</script>

<template>
    <div class="container mb-4">
        <h1>New User</h1>
    </div>
    <div>
         <pre>{{ data }}</pre>
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
                <select class="form-control" id="role" v-model="formDataRef.role">
                    <option value="">Select Role</option>
                    <option value="3">Admin</option>
                    <option value="2">Manager</option>
                    <option value="1">Student</option>
                </select>
            </div>
        </div>
        <div class="mb-parent">
            <div class="mb-2">
                <label for="firstName">First Name</label>
                <input class="form-control" id="firstName" v-model="formDataRef.firstname" type="text" />
            </div>
            <div class="mb-2">
                <label for="lastName">Last Name</label>
                <input class="form-control" id="lastName" v-model="formDataRef.lastname" type="text" />
            </div>
        </div>
        <div class="mb-parent">
            <div class="mb-2">
                <label for="email">Email</label>
                <input class="form-control" id="email" v-model="formDataRef.email" type="email" />
            </div>
            <div class="mb-2">
                <label for="username">Username</label>
                <input class="form-control" id="username" v-model="formDataRef.username" type="text" />
            </div>
        </div>
        <div class="mb-parent">
            <div class="mb-2">
                <label for="password">Password</label>
                <input class="form-control" id="password" v-model="formDataRef.password" type="password" />
            </div>
            <div class="mb-2">
                <label for="repeat-password">Repeat Password</label>
                <input class="form-control" id="repeat-password" v-model="formDataRef.repeatpassword" type="password" />
            </div>
            <p v-if="formDataRef.password !== formDataRef.repeatpassword" style="color:red;">Passwords don't match</p>
        </div>
        <div class="mb-parent">
            <div class="mb-2">
                <label for="studentid">Student Id</label>
                <input class="form-control" id="student_id" v-model="formDataRef.student_id" type="text" />
            </div>
            <div class="mb-2">
                <label for="birthday">Birthday</label>
                <input class="form-control" id="birth_date" v-model="formDataRef.birth_date" type="date" />
            </div>
        </div>
        <div class="">
            <button class="btn btn-primary" @click="onSubmit" type="button">
                Create new user
            </button>
        </div>
    </div>
</template>

<style src="/src/assets/newstudent.css"></style>