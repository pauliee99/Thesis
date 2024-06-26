<script setup>
// @EXERCISE: If user is authenticated redirect to the requested URL.
// @EXERCISE: If user is not authenticated, keep the requested URL and after a successful authentication redirect to the requested resource.
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';
import S3 from 'aws-sdk/clients/s3'

const router = useRouter();
const { setUserData, persistUserData, isAuthenticated, setToken, getToken, getRole } = useApplicationStore();

const loading = ref(false);
const credentials = ref({
    username: '',
    password: '',
});
const passwordMismatch = ref(false);

const password = ref(null);
const repeatPassword = ref(null);
const fname = ref(null);
const lname = ref(null);
const username = ref(null);
const birthdate = ref(null);
const studentid = ref(null);

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
            
            /* @TODO:touta na ginoun .env viarables */
            const s3 = new S3({
                accessKeyId: 'VKYsbj4UVQrZVCmGgWVR',
                secretAccessKey: '52JXYuhvZTKLoO69VULDvF7t6csfrMLEgTng6Jrd',
                endpoint: 'http://localhost:9000',
                s3ForcePathStyle: true,
                signatureVersion: 'v4'
            })

            const params = {
                Bucket: 'profile-pictures',
                Key: file.name,
                Body: file,
                ContentType: file.type
            }

            await s3.upload(params).promise()
            const url = s3.getSignedUrl('getObject', {
                Bucket: 'event-pictures',
                Key: file.name,
                Expires: 60 * 60 * 60 * 60
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

const onFormSubmit = async () => {
    loading.value = true;
    passwordMismatch.value = false;

    console.log('username: ', credentials.value.username, '  password: ', credentials.value.password);

    if (credentials.value.password !== repeatPassword.value) {
        console.error('Passwords do not match');
        passwordMismatch.value = true;
        return;
    }
    console.log('Passwords match');

    await uploadPicture();

    const requestBody = {
        id: 0,
        username: username.value,
        email: credentials.value.username,
        password: credentials.value.password,
        firstname: fname.value,
        lastname: lname.value,
        birth_date: birthdate.value,
        student_id: studentid.value,
        profile_picture: imageUrl.value,
        createdon: '2024-06-01T10:24:25.154Z',
        role: 1,
        disabled: false
    };
    console.log(requestBody);
    fetch('http://localhost:8000/users/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to login');
            }
            return response.json();
        })
        .then(data => {
            setUserData(data);
            persistUserData();
            console.log("redirecting...");
            router.push({ name: 'profile' });
            
        })
        .catch((err) => {
            console.warn(err);
            passwordMismatch.value = true;
        })
        .finally(() => {
            loading.value = false;
        });
};

onBeforeMount(() => {
    if (isAuthenticated === true) {
        router.push({ name: 'home' });
    }
});
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-4">
                    <div class="mb-4">
                        <h1 class="fs-3">Register</h1>
                    </div>
                    <div class="spinner-border" role="status" v-if="loading">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <form v-else @submit.prevent="onFormSubmit">
                        <div class="mb-2" v-if="passwordMismatch">
                            <div class="alert alert-danger" role="alert">
                                Passwords mismatch!
                            </div>
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <div class="setup-picture">
                                <form @submit.prevent="uploadPicture">
                                <img v-if="uploadedImage" :src="uploadedImage" id="uploaded" alt="Uploaded picture" /> <!-- Uploaded picture goes here -->
                                <div class="picture">
                                    <input type="file" name="event_picture" id="event_picture" @change="previewPicture" />
                                    <i class="fas fa-camera" @click="triggerFileInput"></i>
                                    <h3>Choose your picture</h3>
                                    <div class="clearfix"></div>
                                </div>
                                <!-- <button class="btn btn-dark mt-15">Upload Picture</button> -->
                                </form>
                            </div>
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="fanameFormControl" class="form-label mb-1"
                                >First Name</label
                            >
                            <input
                                v-model="fname"
                                type="text"
                                class="form-control"
                                id="fnameFormControl"
                            />
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="lanameFormControl" class="form-label mb-1"
                                >Last Name</label
                            >
                            <input
                                v-model="lname"
                                type="text"
                                class="form-control"
                                id="lnameFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="usernameFormControl" class="form-label mb-1"
                                >Email address</label
                            >
                            <input
                                v-model="credentials.username"
                                type="text"
                                class="form-control"
                                id="emailFormControl"
                            />
                        </div>
                        <div class="mb-2" style="display: inline-block;">
                            <label for="usernameFormControl" class="form-label mb-1"
                                >Username</label
                            >
                            <input
                                v-model="username"
                                type="text"
                                class="form-control"
                                id="usernameFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="passwordFormControl" class="form-label mb-1"
                                >Password</label
                            >
                            <input
                                v-model="credentials.password"
                                type="password"
                                class="form-control"
                                id="passwordFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="repeatPasswordFormControl" class="form-label mb-1"
                                >Repeat Password</label
                            >
                            <input
                                v-model="repeatPassword"
                                type="password"
                                class="form-control"
                                id="repeatPasswordFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="birthdateFormControl" class="form-label mb-1"
                                >Birth Date</label
                            >
                            <input
                                v-model="birthdate"
                                type="date"
                                class="form-control"
                                id="birthdateFormControl"
                            />
                        </div>
                        <div class="mb-2">
                            <label for="studentidFormControl" class="form-label mb-1"
                                >Student ID</label
                            >
                            <input
                                v-model="studentid"
                                type="number"
                                class="form-control"
                                id="studentidFormControl"
                            />
                        </div>
                        <button @click="onFormSubmit" type="submit" class="btn btn-primary">
                            Register
                            <span class="fst-italic" v-if="credentials.username"
                                >as {{ credentials.username }}</span
                            >
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.setup-picture {
    form {
      margin-top: 20px !important;
      width: 70%;
      margin: auto;
      img {
        width: 400px;
        height: 350px;
        display: none;
        margin: auto;
      }
      .picture {
        transition: .3s;
        position: relative;
        text-align: center;
        padding: 10px 30px;
        border: 3px dashed #ddd;
        background-color: #f1f1f1;
        border-radius: 5px;
        &:hover {
          background-color: #263238;
          color: #aaa;
          border: 3px solid #263238
        }
        &:hover i {
          color: #aaa;
        }
        input {
          width: 100%;
          height: 100%;
          opacity: 0;
          position: absolute;
          top: 0;
          left: 0;
        }
        h3, i {
          float: left;
        }
        i {
          font-size: 2.5em;
          margin-right: 15px;
          color: #263238;
        }
        h3 {
          margin-top: 10px;
          font-weight: 100;
        }
      }
      button {
        font-family: 'PT Sans', sans-serif;
        border: 2px solid #3498db;
        padding: 10px 25px;
        color: #3498db;
        background-color: transparent;
        font-weight: bold;
        border-radius: 50px;
        &:hover {
          background-color: rgba(52, 152, 219, .2);
        }
      }
    }
  }
#uploaded {
    display: none;
}



.setup-picture {
  text-align: center;
}

#uploaded {
  max-width: 100%;
  height: auto;
}

.picture {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}



.picture .fa-camera {
  font-size: 3rem;
  cursor: pointer;
}

.btn {
  padding: 10px 20px;
  cursor: pointer;
}
</style>