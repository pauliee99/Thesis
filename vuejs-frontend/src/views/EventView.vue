<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const eventIdRef = ref(null);

onMounted(() => {
    eventIdRef.value = route.params.id;
    console.log(eventIdRef.value);
});
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <RouterLink class="small" :to="{ name: 'events' }"
                            >Back to Events</RouterLink
                        >
                        <h1 class="fs-3">Event #{{ eventIdRef }}</h1>
                    </div>
                    <!-- <div class="mb-4">
                        <ul class="nav border">
                            <li class="nav-item">
                                <RouterLink
                                    class="nav-link"
                                    :to="{ name: 'event-details', params: { id: eventIdRef } }"
                                    >Details</RouterLink
                                >
                            </li>
                            <li class="nav-item">
                                <RouterLink
                                    class="nav-link"
                                    :to="{ name: 'course-students', params: { id: eventIdRef } }"
                                    >Courses test</RouterLink
                                >
                            </li>
                        </ul>
                    </div> -->
                    <div>
                        <router-view></router-view>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
