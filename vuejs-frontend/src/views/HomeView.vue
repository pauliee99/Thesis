<script setup>
import { useApplicationStore } from '@/stores/application.js';
const { userData } = useApplicationStore();
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3">Home</h1>
                    </div>
                    <div>
                        <p>
                            Logged in as: <strong>{{ userData?.username }}</strong>
                        </p>
                        <ul>
                            <li>
                                <RouterLink :to="{ name: 'events' }">Manage Events</RouterLink>
                            </li>
                            <li>
                                <RouterLink :to="{ name: 'students' }">Manage Students</RouterLink>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
