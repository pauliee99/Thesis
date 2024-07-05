<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useRemoteData } from '@/composables/useRemoteData.js';
import { useApplicationStore } from '@/stores/application.js';

const router = useRouter();
const route = useRoute();

const { userData } = useApplicationStore();
const { getToken } = useApplicationStore();
const token = getToken()?.access_token.access_token;

const studentIdRef = ref(null);
studentIdRef.value = route.params.username;
const authRef = ref(true);
const userIdRef = ref(null);
const urlRef = computed(() => {
    return 'http://localhost:8000/users/' + userIdRef.value;
});
const authRef2 = ref(true);
const methodRef = ref('PUT');
const showpopup = ref(false);

const { performRequest } = useRemoteData(urlRef, authRef, methodRef);
const onSubmit = () => {
    performRequest({ token })
};
</script>

<template>
    <div>
        <p>
            Do you really want to delete user?
        </p>
        <RouterLink
            class="nav-link"
            :to="{ name: 'student-details', params: { id: studentIdRef } }"
            ><button class="btn btn-primary" @click="onSubmit" type="button">Update Record</button></RouterLink
        >
        <RouterLink
            class="nav-link"
            :to="{ name: 'student-details', params: { id: studentIdRef } }"
            ><button class="btn btn-primary" @click="onSubmit" type="button">Update Record</button></RouterLink
        >
    </div>
</template>
