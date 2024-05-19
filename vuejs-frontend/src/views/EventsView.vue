<script setup>
import { onMounted, ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';

const { getToken } = useApplicationStore();

const urlRef = ref('http://localhost:8000/events');
const authRef = ref(true);
const { data, loading, performRequest } = useRemoteData(urlRef, authRef);
console.log(data);
const token = getToken()?.access_token.access_token;
const showpopup = ref(false);

onMounted(() => {
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
                        <h1 class="fs-3" @click="showpopup=false">Events</h1>
                    </div>
                    <div class="container">
                        <div v-if="data">
                            <div class="gallery" v-for="event in data" :key="event.id">
                                <router-link :to="{ name: 'event-details', params: { id: event.id } }">
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
                                </router-link>
                            </div>
                        </div>
                        <div v-else>
                            <p>No events available at the moment</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

<div class="floating-container" @click="showpopup = true">
  <div class="floating-button">+</div>
  <div class="element-container">
  </div>
</div>
<!-- Popup code here. -->
<div class="overlay" id="overlay" v-if="showpopup==true">
    <!-- Content inside the overlay -->
    <div class="content">
      <a href="#" class="close-button" @click="showpopup = false">&#10006;</a>
      <h2>Do you really want to create a new Event?</h2>
      <div class="response-container">
        <button id="cancel-button" @click="showpopup = false">Cacnel</button>
        <router-link :to="{ name: 'event-new' }">
            <button id="continue-button" :to="{ name: 'event-new' }">Continue</button>
        </router-link>
      </div>
    </div>
  </div>

</template>

<!-- 
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
</style> -->


<style src="../assets/events.css"></style>