<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRemoteData } from '@/composables/useRemoteData.js';

const router = useRouter();
const route = useRoute();

const studentIdRef = ref(null);
studentIdRef.value = route.params.username;
const urlRef = computed(() => {
    return 'http://localhost:8000/users/' + studentIdRef.value;
});
console.log(urlRef)
const authRef = ref(false); //@TODO: na to kamo true molis vao je to auth tou backend
const { data, loading, performRequest } = useRemoteData(urlRef, authRef);

onMounted(() => {
    studentIdRef.value = route.params.username;
    performRequest() //@TODO: na valo to token molis saso to authendication tou endpoint
});
</script>

<template>
    <div>
        <table class="table">
            <thead>
                <tr>
                    <th>Field Name</th>
                    <th>Field Value</th>
                </tr>
            </thead>
            <tbody v-if="loading">
                <tr>
                    <td colspan="2">Loading...</td>
                </tr>
            </tbody>
            <tbody v-if="data">
                <tr>
                    <th>First Name</th>
                    <td>{{ data.firstname }}</td>
                </tr>
                <tr>
                    <th>Last Name</th>
                    <td>{{ data.lastname }}</td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td>{{ data.email }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
