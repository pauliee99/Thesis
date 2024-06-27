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

const uploadedImage = ref('')
const statusMessage = ref('No uploads')
const imageUrl = ref('')

function previewPicture(event) {
    const fileInput = event.target
    const file = fileInput.files?.[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
            if (typeof e.target?.result === 'string') {
                uploadedImage.value = e.target.result
                console.log(uploadedImage.value)  // Print the base64 image data to the console
            }
        }
        reader.readAsDataURL(file)
    }
}

async function uploadPicture() {
    const fileInput = document.getElementById('event_picture')
    if (fileInput && fileInput.files?.length) {
        const file = fileInput.files[0]
        try {
            const presignedUrlResponse = await fetch(`/presignedUrl?name=${file.name}`)
            const presignedUrl = await presignedUrlResponse.text()

            const s3 = new S3({
                accessKeyId: 'VKYsbj4UVQrZVCmGgWVR',
                secretAccessKey: '52JXYuhvZTKLoO69VULDvF7t6csfrMLEgTng6Jrd',
                endpoint: 'http://localhost:9000',
                s3ForcePathStyle: true,
                signatureVersion: 'v4'
            })

            const params = {
                Bucket: 'event-pictures',
                Key: file.name,
                Body: file,
                ContentType: file.type
            }

            await s3.upload(params).promise()
            const url = s3.getSignedUrl('getObject', {
                Bucket: 'event-pictures',
                Key: file.name,
                Expires: 60 * 60 * 60
            })
            imageUrl.value = url
            console.log(url)
            statusMessage.value = `Uploaded ${file.name}.`
        } catch (error) {
            console.error('Error uploading file:', error)
            statusMessage.value = `Error uploading ${file.name}.`
        }
    } else {
        console.error('No file selected')
    }
}

function triggerFileInput() {
    const fileInput = document.getElementById('event_picture')
    if (fileInput) {
        fileInput.click()
    } else {
        console.error('File input element not found')
    }
}

const onSubmit = async () => {
    await uploadPicture();
    formDataRef.value.createdby = getUserData()?._value.username;
    formDataRef.value.createdon = "2024-02-22T00:00:00";
    formDataRef.value.picture = imageUrl.value;
    const response = performRequest({ token });
    if (response.status === 403) {
        console.warn('Access forbidden. Redirecting to login.');
        router.push({ name: 'login' });
    } else if (response.success) {
        console.log('Event created successfully.');
    } else {
        console.log('Failed to create event:', response.message);
    }
};
</script>
<style src="../assets/createevents.css"></style>
<template>
    <RouterLink class="small" :to="{ name: 'events' }"
                            >Back to Events</RouterLink
                        >
    <div class="container mb-4">
        <h1>New Event</h1>
    </div>
    <div>
        <pre>{{ data }}</pre>
    </div>
    <div class="container mb-4" >
        <div id="container-add-event-form-field">
            <div class="mb-2">
                <div class="setup-picture">
                    <form @submit.prevent="uploadPicture">
                    <img v-if="uploadedImage" :src="uploadedImage" id="uploaded" alt="Uploaded picture" /> <!-- Uploaded picture goes here -->
                    <div class="picture">
                        <input type="file" name="event_picture" id="event_picture" @change="previewPicture" />
                        <i class="fas fa-camera" @click="triggerFileInput"></i>
                        <h3>Choose your picture</h3>
                        <div class="clearfix"></div>
                    </div>
                    <button class="btn btn-dark mt-15">Upload Picture</button>
                    </form>
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
