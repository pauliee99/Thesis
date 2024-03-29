<script setup>
import { onMounted, ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';

const { getToken } = useApplicationStore();

const urlRef = ref('http://localhost:8000/events');
const authRef = ref(true);
const { data, loading, performRequest } = useRemoteData(urlRef, authRef);

const token = getToken()?.access_token.access_token;

onMounted(() => {
    performRequest({ token });
});
</script>
<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3">Events</h1>
                    </div>
                    <div class="gallery">
                        <div class="event" v-for="event in data" :key="event.id">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>First Name</th>
                                        <th>Last Name</th>
                                        <th>Email</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{{ event.id }}</td>
                                        <td>{{ event.displayname }}</td>
                                        <td>{{ event.location }}</td>
                                        <td>{{ event.price }}</td>
                                        <td>
                                            <RouterLink
                                                :to="{
                                                    name: 'event-details',
                                                    params: { id: event.id }
                                                }"
                                                >Display</RouterLink
                                            >
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
    .gallery {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: space-between;
    }
    .event {
        width: calc(33.33% - 20px);
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>


<style src="../assets/events.css"></style>