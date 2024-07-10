<script setup>
import { ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';
import S3 from 'aws-sdk/clients/s3'
const applicationStore = useApplicationStore();
const { getUserData } = useApplicationStore();
const { getToken } = useApplicationStore();

const formDataRef = ref({
    displayname: '',
    picture: '',
    location: '',
    start_time: '',
    end_time: '',
    price: '',
    description: '',
    createdon: '',
    createdby: ''
});
const urlRef = ref('http://localhost:8000/events');
const authRef = ref(true);
const methodRef = ref('POST');

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);
const token = getToken()?.access_token.access_token;

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

const onSubmit = async () => {
    await uploadPicture();
    formDataRef.value.createdby = getUserData()?._value.username;
    formDataRef.value.createdon = "2024-02-22T00:00:00";
    formDataRef.value.picture = imageUrl.value;
    const response = performRequest({ token });
    // if (response.status === 403) {
    //     console.warn('Access forbidden. Redirecting to login.');
    //     router.push({ name: 'login' });
    // } else if (response.success) {
    //     console.log('Event created successfully.');
    // } else {
    //     console.log('Failed to create event:', response.message);
    // }
};
</script>
<style src="../assets/createevents.css"></style>
<template>
    
    <!-- <div class="container mb-4">
        
    </div> -->
    <!-- <div>
        <pre>{{ data }}</pre>
    </div> -->
    <div class="container mb-4" >
        <RouterLink class="small" :to="{ name: 'events' }"
                            >Back to Events</RouterLink
                        >
        <h1>New Event</h1>
        <div id="container-add-event-form-field">
            <div class="mb-2">
                <div class="setup-picture">
                    <div class="profileviewcircle" @click="triggerFileInput">
                            <img id="edit-profilepicture" class="profile-img-n" src="http://127.0.0.1:9001/api/v1/buckets/icons/objects/download?preview=true&prefix=edit-profile-picture.svg&version_id=null">
                            <img :src="defaultProfilePictureUrl" class="profile-img">
                        </div>
                        <input id="event_picture_ep" type="file" ref="fileInputRef" @change="previewPicture" style="display: none;" />
                </div>
            </div>
            <div class="mb-2">
                <label for="eventName">Event Name</label>
                <input
                    class="form-control"
                    id="eventtName"
                    v-model="formDataRef.displayname"
                    type="text"
                />
            </div>
            <div class="mb-2">
                <label for="location">Location</label>
                <input class="form-control" id="location" v-model="formDataRef.location" type="text" />
            </div>
            <div class="mb-2">
                <label for="description">Description</label>
                <textarea class="form-control" id="description" v-model="formDataRef.description" type="text" ></textarea>
            </div>
            <div class="mb-2">
                <label for="price">Price</label>
                <input class="form-control" id="price" v-model="formDataRef.price" type="number" min="0" />
            </div>
            <div class="mb-2">
                <label for="start_time">Start Time</label>
                <input class="form-control" id="start_time" v-model="formDataRef.start_time" type="datetime-local" />
            </div>
            <div class="mb-2">
                <label for="end_time">End Time</label>
                <input class="form-control" id="end_time" v-model="formDataRef.end_time" type="datetime-local" />
            </div>
            <div class="">
                <button class="btn btn-primary" @click="onSubmit" type="button">
                    Create new event
                </button>
            </div>
        </div>
    </div>
</template>
