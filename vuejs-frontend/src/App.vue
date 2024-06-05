<script setup>
import { onBeforeMount } from 'vue';
import { RouterView } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';
import AppHeader from '@/components/AppHeader.vue';
import AppFooter from '@/components/AppFooter.vue';

const { loadUserData } = useApplicationStore();

onBeforeMount(() => {
    // If this method is non-blocking, add a loader.
    loadUserData();
});
</script>

<template style="height:100vh;">
    <AppHeader />
    <RouterView />
    <AppFooter />
</template>
