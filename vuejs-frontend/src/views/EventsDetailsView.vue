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
// const { data: userEventData, performRequest:fetchUserEvents } = useRemoteData(urlRefUsrEv, authRef);
const isEnrolled = ref('')
const fetchUserEvents = async () => {
    try {
        console.log('http://localhost:8000/userevents/' + userIdRef.value + '/' + eventIdRef.value)
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
    user: '',
    event: ''
});
const urlRefAdd = ref('http://localhost:8000/userevents/');
const methodRef = ref('POST');

const { data: newEventData, performRequest:enrollToEvent } = useRemoteData(urlRefAdd, authRef, methodRef, formDataRef);
watch(eventData, (newData) => {
    if (newData) {
        formDataRef.value.user = getUserData()?._value.id;
        formDataRef.value.event = newData.id;
    }
});
const isUserEnrolled = computed(() => {
    return true;
});
console.log(isUserEnrolled)
const onSubmit = () => {
    enrollToEvent({ token });
    isEnrolled.value = true
};
const urlRefDel = ref('http://localhost:8000/userevents/');
const methodRefDel = ref('DELETE');
const { data: deleteEventData, performRequest:unenrollToEvent } = useRemoteData(urlRefDel, authRef, methodRefDel, formDataRef);
const onDelete = () => {
    unenrollToEvent({ token });
    isEnrolled.value = false
};
onMounted(async () => {
    eventIdRef.value = route.params.id;
    userIdRef.value = getUserData()?._value.id;
    // fetchUserEvents({ token });
    await fetchUserEvents();
    fetchEventDetails({ token });
    fetchEventUsers({ token });
    // await fetchUserEvents();
    fetchUserEvents({ token });
    // setTimeout(function(){
    //     console.log(userEventData.value);
    // }, 2000);
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
                    <div class="container">
                        <div v-if="eventData">
                            <table class="table">
                                <tbody>
                                    <tr>
                                        <th>ID</th>
                                        <td>{{ eventData.id }}</td>
                                    </tr>
                                    <tr>
                                        <th>Location</th>
                                        <td>{{ eventData.location }}</td>
                                    </tr>
                                    <tr>
                                        <th>Price</th>
                                        <td>{{ eventData.price }}</td>
                                    </tr>
                                    <tr>
                                        <th>Description</th>
                                        <td>{{ eventData.description }}</td>
                                    </tr>
                                    <tr>
                                        <th>Created On</th>
                                        <td>{{ eventData.createdon }}</td>
                                    </tr>
                                    <tr>
                                        <th>Display Name</th>
                                        <td>{{ eventData.displayname }}</td>
                                    </tr>
                                    <tr>
                                        <th>End Time</th>
                                        <td>{{ eventData.end_time }}</td>
                                    </tr>
                                    <tr>
                                        <th>Start Time</th>
                                        <td>{{ eventData.start_time }}</td>
                                    </tr>
                                    <tr>
                                        <th>Picture</th>
                                        <td>{{ eventData.picture }}</td>
                                    </tr>
                                    <tr>
                                        <th>Created By</th>
                                        <td>{{ eventData.createdby }}</td>
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
                            <button class="btn-enroll-user-event" @click="onSubmit" v-if="!isEnrolled">join</button>
                            <button class="btn-unenroll-user-event" @click="onDelete" v-else>snob</button>
                        </div>
                        <div v-else-if="userData && userData.length > 0">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>User ID</th>
                                        <th>Name</th>
                                        <th>Email</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in userData" :key="user.id">
                                        <td>{{ user.id }}</td>
                                        <td>{{ user.name }}</td>
                                        <td>{{ user.email }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else>
                            <p>No users attending this event.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
