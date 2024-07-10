<script setup>
import { ref, computed } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
import S3 from 'aws-sdk/clients/s3';

const fileInputRef = ref(null);
const uploadedImage = ref('')
const statusMessage = ref('No uploads')
const imageUrl = ref('')
const imageName = ref('')
async function uploadPicture() {
    const fileInput = document.getElementById('event_picture_ep')
    if (fileInput && fileInput.files?.length) {
        const file = fileInput.files[0]
        console.log(file)
        try { 
            const filename = generateRandomString(20) + '.' + file.name.split('.').pop(); //@TODO: needs testing
            console.log(filename)
            const presignedUrlResponse = await fetch(`/presignedUrl?name=${filename}`)
            const presignedUrl = await presignedUrlResponse.text()

            const s3 = new S3({
                accessKeyId: import.meta.env.VITE_ACCESS_KEY,
                secretAccessKey: import.meta.env.VITE_SECRET_ACCESS_KEY,
                endpoint: import.meta.env.VITE_ENDPOINT,
                s3ForcePathStyle: import.meta.env.VITE_FORCE_PATH_STYLE,
                signatureVersion: import.meta.env.VITE_SIGNATURE_VERSION
            })

            const params = {
                Bucket: 'profile-pictures',
                Key: filename,
                Body: file,
                ContentType: file.type
            }
            console.log("here");
            await s3.upload(params).promise()
            console.log("here");
            const url = s3.getSignedUrl('getObject', {
                Bucket: 'profile-pictures',
                Key: filename,
                Expires: 60 * 60 * 60
            })
            imageUrl.value = url
            console.log(url)
            console.log(filename)
            imageName.value = filename
            statusMessage.value = `Uploaded ${filename}.`
        } catch (error) {
            console.error('Error uploading file:', error)
            statusMessage.value = `Error uploading ${file.name}.`
        }
    } else {
        console.error('No file selected')
    }
}
async function previewPicture(event) {
    const fileInput = event.target
    const file = fileInput.files?.[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
            if (typeof e.target?.result === 'string') {
                uploadedImage.value = e.target.result
                // console.log(uploadedImage.value)  // Print the base64 image data to the console
            }
        }
        reader.readAsDataURL(file)
    }
}
const triggerFileInput = () => {
  fileInputRef.value.click();
};
const randomString = ref('');
const generatedStrings = new Set();
const generateRandomString = (n) => {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result;

    do {
    result = '';
    for (let i = 0; i < n; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    } while (generatedStrings.has(result));

    generatedStrings.add(result);
    randomString.value = result;
    return randomString.value
};
// const defaultProfilePictureUrl = computed(() => {
//     if (uploadedImage.value) {
//         return uploadedImage.value
//     } else {
//         if (userData.profile_picture) {
//             return userData.profile_picture;
//         } else {
//             return 'http://127.0.0.1:9001/api/v1/buckets/profile-pictures/objects/download?preview=true&prefix=cHJvZmlsZS1kZWZhdWx0LnBuZw==&version_id=null';
//         }
//     }
// });

const formDataRef = ref({
    id: 0,
    firstname: '',
    lastname: '',
    email: '',
    username: '',
    password: '',
    birth_date: '',
    profile_picture: 'default.png',
    student_id: null,
    role: null,
    createdon: '2024-05-04T15:58:19.765Z',
    disabled: false,
});
const urlRef = ref('http://localhost:8000/users/signup');
const authRef = ref(true);
const methodRef = ref('POST');

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);

const onSubmit = async () => {
    await uploadPicture(); 
    formDataRef.value.profile_picture = imageName.value;
    console.log(imageName.value);
    performRequest(formDataRef?._rawValue);
};
</script>

<template>
    <div class="bg-body-tertiary">
    <div class="container mb-4">
        <RouterLink class="small" :to="{ name: 'students' }"
                            >Back to Users</RouterLink
                        > 
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
                    <div class="profileviewcircle" @click="triggerFileInput">
                            <img id="edit-profilepicture" class="profile-img-n" src="http://127.0.0.1:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=edit-profile-picture.svg&version_id=null">
                            <img :src="defaultProfilePictureUrl" alt="Profile Picture" class="profile-img">
                        </div>
                        <input id="event_picture_ep" type="file" ref="fileInputRef" @change="previewPicture" style="display: none;" />
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
            
            <RouterLink
            class="nav-link"
            :to="{ name: 'students' }"
            ><button class="btn btn-primary" @click="onSubmit" type="button">
                Create new user
            </button></RouterLink>
        </div>
    </div>
</div>
</template>

<style src="/src/assets/newstudent.css"></style>