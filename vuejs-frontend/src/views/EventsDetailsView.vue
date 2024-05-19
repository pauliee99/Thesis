<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';

const { getToken } = useApplicationStore();
const token = getToken()?.access_token.access_token;
const router = useRouter();
const route = useRoute();

const eventIdRef = ref(null);
const urlRef = computed(() => {
    return 'http://localhost:8000/events/' + eventIdRef.value;
});
const authRef = ref(true);
const { data, loading, performRequest } = useRemoteData(urlRef, authRef);
onMounted(() => {
    console.log(token);
    eventIdRef.value = route.params.id;
    console.log(eventIdRef.value);
    performRequest({ token });
});
</script>
<template>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3" @click="showpopup=false">Event Details</h1>
                    </div>
                    <div class="container">
                        <div v-if="data">
                            <table class="table">
                                <tbody>
                                    <tr>
                                        <th>ID</th>
                                        <td>{{ data.id }}</td>
                                    </tr>
                                    <tr>
                                        <th>Location</th>
                                        <td>{{ data.location }}</td>
                                    </tr>
                                    <tr>
                                        <th>Price</th>
                                        <td>{{ data.price }}</td>
                                    </tr>
                                    <tr>
                                        <th>Description</th>
                                        <td>{{ data.description }}</td>
                                    </tr>
                                    <tr>
                                        <th>Created On</th>
                                        <td>{{ data.createdon }}</td>
                                    </tr>
                                    <tr>
                                        <th>Display Name</th>
                                        <td>{{ data.displayname }}</td>
                                    </tr>
                                    <tr>
                                        <th>End Time</th>
                                        <td>{{ data.end_time }}</td>
                                    </tr>
                                    <tr>
                                        <th>Start Time</th>
                                        <td>{{ data.start_time }}</td>
                                    </tr>
                                    <tr>
                                        <th>Picture</th>
                                        <td>{{ data.picture }}</td>
                                    </tr>
                                    <tr>
                                        <th>Created By</th>
                                        <td>{{ data.createdby }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-else>
                            <p>No event data available at the moment</p>
                        </div>
                    </div>
                    <div>
                        <button>Enroll to this event</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
