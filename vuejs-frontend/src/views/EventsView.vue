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
                    <div class="container">
                        <div class="gallery" v-for="event in data" :key="event.id">
                            <a id="event-img" :href="'/event/' + event.id" target="_blank">
                                <!-- <img :src="event.imageSrc" :alt="event.displayname" width="600" height="400"> -->
                                <img :src="event.imageSrc ? event.imageSrc : '../../public/default.png'"
                                             :alt="event.displayname"
                                             width="600" height="400"
                                             :style="{ width: '100%', height: 'auto', marginBottom: '10px' }">
                            </a>
                            <div class = "desc">
                                <div class="desc">Title: {{ event.displayname }}</div>
                                <div id="event-price">
                                    <p v-if="event.price === 0" class="desc">Price: Free</p>
                                    <p v-else class="desc">Price: {{ event.price }}€</p>
                                </div>
                            </div>
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