<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';
const applicationStore = useApplicationStore();
const { getUserData } = useApplicationStore();
const { getToken } = useApplicationStore();

const token = getToken()?.access_token.access_token;
const router = useRouter();
const route = useRoute();

const eventIdRef = ref(null);
const userIdRef = ref(null);
const urlRef = computed(() => {
    return 'http://localhost:8000/events/' + eventIdRef.value;
});
const urlRefUsr = computed(() => {
    return 'http://localhost:8000/userevents/event/' + eventIdRef.value;
});
const urlRefUsrEv = computed(() => {
    return 'http://localhost:8000/userevents/' + userIdRef.value + '/' + eventIdRef.value;
});
const authRef = ref(true);
const { data: eventData, loading, performRequest:fetchEventDetails } = useRemoteData(urlRef, authRef);
const { data: userData, performRequest:fetchEventUsers } = useRemoteData(urlRefUsr, authRef);
// const { data: currUserEventData, performRequest:fetchCurrUserEvent } = useRemoteData(urlRefUsrEv, authRef);
const isEnrolled = ref('')
const fetchUserEvents = async () => {
    try {
        // console.log('http://localhost:8000/userevents/' + userIdRef.val ue + '/' + eventIdRef.value)
        const response = await fetch('http://localhost:8000/userevents/' + userIdRef.value + '/' + eventIdRef.value, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });
        if (response.ok) {
            // setUserData(response.data);
            // persistUserData();
            const data = await response.json();
            console.log(data)
            if (data.length) isEnrolled.value = true
            else isEnrolled.value = false
        } else {
            console.error('Failed to fetch user data:', response);
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
};


const formDataRef = ref({
    id: '',
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
const urlRefEv = computed(() => {
    return 'http://localhost:8000/events/' + eventIdRef.value;
});
const methodRef = ref('PUT');
const { data: newEventData, performRequest:PutEvent } = useRemoteData(urlRefEv, authRef, methodRef, formDataRef);
const onSubmit = () => {
    formDataRef.value = eventData.value
    console.log(formDataRef.value)
    PutEvent({ token });
};
const urlRefDel = computed(() => {
    return 'http://localhost:8000/userevents/' + eventIdRef.value + '/' + userIdRef.value;
});
const methodRefDel = ref('DELETE');
const { data: deleteEventData, performRequest:unenrollToEvent } = useRemoteData(urlRefDel, authRef, methodRefDel, formDataRef);
const onDelete = (userId) => {
    userIdRef.value = userId
    unenrollToEvent({ token });
    fetchEventUsers({ token });
    userData.value = userData.value.filter(user => user.id !== userId);
};
onMounted(async () => {
    eventIdRef.value = route.params.id;
    userIdRef.value = getUserData()?._value.id;
    await fetchUserEvents();
    fetchEventDetails({ token });
    fetchEventUsers({ token });
    console.log(userData);
    fetchUserEvents({ token });
});
</script>
<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3" @click="showpopup=false">Event Details</h1>
                    </div>
                    <div class="container-tmp">
                        <div v-if="eventData">
                            <table class="table">
                                <tbody>
                                    <tr>
                                        <th>Display Name</th>
                                        <td><input class="form-control" id="id" v-model="eventData.displayname" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>Location</th>
                                        <td><input class="form-control" id="id" v-model="eventData.location" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>Price</th>
                                        <td><input class="form-control" id="id" v-model="eventData.price" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>Description</th>
                                        <td><input class="form-control" id="id" v-model="eventData.description" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>End Time</th>
                                        <td><input class="form-control" id="id" v-model="eventData.end_time" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>Start Time</th>
                                        <td><input class="form-control" id="id" v-model="eventData.start_time" type="text" /></td>
                                    </tr>
                                    <tr>
                                        <th>Picture</th>
                                        <td><input class="form-control" id="id" v-model="eventData.picture" type="text" /></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else>
                            <p>No event data available at the moment</p>
                        </div>
                    </div>
                    <div>
                        <div v-if="getUserData()?._value.role === 'Student' ||getUserData()?._value.role === 1">
                            <button class="btn-enroll-user-event" @click="onSubmit" v-if="!isEnrolled">Join</button>
                            <button class="btn-unenroll-user-event" @click="onDelete" v-else>Snob</button>
                        </div>
                        <div v-else-if="userData && userData.length > 0">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>User ID</th>
                                        <th>Name</th>
                                        <th>Email</th>
                                        <th>Remove</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in userData" :key="user.id">
                                        <td>{{ user.id }}</td>
                                        <td>{{ user.name }}</td>
                                        <td>{{ user.email }}</td>
                                        <td><span class="close" @click="onDelete(user.id)">&times;</span></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else>
                            <p>No users attending this event.</p>
                        </div>
                    </div>
                    <RouterLink :to="{ name: 'event-details' }">
                                <button class="btn btn-primary" type="button">
                                    Cancel
                                </button>
                            </RouterLink>
                    <RouterLink :to="{ name: 'event-details' }" style="margin-left: 10%;">
                                <button class="btn btn-primary" @click="onSubmit" type="button">
                                    Save
                                </button>
                            </RouterLink>
                </div>
            </div>
        </div>
    </div>

</template>
<style scoped>
.btn-enroll-user-event {
  width: 150px;
  background: #27ae60;
  font-weight: bold;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 12px 20px;
  margin: 10px 5px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-enroll-user-event:hover, 
.btn-enroll-user-event:focus {
  background: #1e8449;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  outline: none;
}

.btn-unenroll-user-event {
  width: 150px;
  background: #ae2727;
  font-weight: bold;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 12px 20px;
  margin: 10px 5px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-unenroll-user-event:hover, 
.btn-unenroll-user-event:focus {
  background: #841e1e;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  outline: none;
}
</style>
