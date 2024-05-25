<script setup>
import { ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';
const applicationStore = useApplicationStore();
const { getUserData } = useApplicationStore();
const { getToken } = useApplicationStore();

const formDataRef = ref({
    firstName: '',
    lastName: '',
    email: ''
});
const urlRef = ref('http://localhost:8000/events');
const authRef = ref(true);
const methodRef = ref('POST');

const { data, performRequest } = useRemoteData(urlRef, authRef, methodRef, formDataRef);
const token = getToken()?.access_token.access_token;

const onSubmit = () => {
    formDataRef.value.createdby = getUserData()?._value.username;
    formDataRef.value.createdon = "2024-02-22T00:00:00";
    formDataRef.value.picture = null;
    performRequest({ token });
};

// function readURL() {
// 	var $input = $(this);
//     if (this.files && this.files[0]) {
//         var reader = new FileReader();
//         reader.onload = function(e) {
//             $input.next('.blah').attr('src', e.target.result).show();
//         }
//         reader.readAsDataURL(this.files[0]);
//     }
// }
// $(".imgInp").change(readURL);
Vue.component('setup-picture', {
    data() {
        return {
        uploadedImageUrl: null,  // to store the URL of the uploaded picture
        selectedFile: null       // to store the selected file
        };
    },
    methods: {
    previewPicture(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.uploadedImageUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    uploadPicture() {
        if (this.selectedFile) {
            const formData = new FormData();
            formData.append('event_picture', this.selectedFile);

            // Replace the URL below with your actual API endpoint
            fetch('/your-api-endpoint', {
            method: 'POST',
            body: formData,
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            })
            .catch((error) => {
            console.error('Error:', error);
            });
        } else {
            alert('Please select a picture first.');
        }
    }},
    template: `
        <div class="setup-picture">
        <form @submit.prevent="uploadPicture">
            <img :src="uploadedImageUrl" id="uploaded" alt="Uploaded picture" v-if="uploadedImageUrl">
            <div class="picture">
            <input type="file" name="event_picture" id="event_picture" @change="previewPicture">
            <i class="fas fa-camera"></i>
            <h3>Choose your picture</h3>
            <div class='clearfix'></div>
            </div>
            <button class='btn btn-dark mt-15'>Upload Picture</button>
        </form>
        </div>
    `
});
new Vue({
  el: '#app'
});
</script>
<style src="../assets/createevents.css"></style>
<template>
    <div class="container mb-4">
        <h1>New Event</h1>
    </div>
    <div>
        <pre>{{ data }}</pre>
    </div>
    <div class="container mb-4">
        <div class="mb-2">
            <div id="app">
                <setup-picture></setup-picture>
            </div>
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
</template>
