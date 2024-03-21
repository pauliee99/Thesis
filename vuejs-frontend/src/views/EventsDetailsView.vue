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
    <div>
        <table class="table">
            <tbody v-if="data">
                <tr>
                    <th>Title</th>
                    <td>{{ data }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
