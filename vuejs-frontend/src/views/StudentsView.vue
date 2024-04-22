<script setup>
import { onMounted, ref } from 'vue';
import { useRemoteData } from '@/composables/useRemoteData.js';

const urlRef = ref('http://localhost:8000/users');
const authRef = ref(false); //@TODO: na to kamo true molis vao je to auth tou backend
const { data, loading, performRequest } = useRemoteData(urlRef, authRef);

onMounted(() => {
    performRequest(); //@TODO: na valo to token molis saso to authendication tou endpoint
});
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-12">
                    <div class="mb-4">
                        <h1 class="fs-3">Students</h1>
                    </div>
                    <div style="max-height: 75%; overflow-y: auto;">
                        <table class="table" >
                            <thead style="position: sticky; top: 0;">
                                <tr>
                                    <th>ID</th>
                                    <th>First Name</th>
                                    <th>Last Name</th>
                                    <th>Email</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody v-if="loading">
                                <tr>
                                    <td colspan="5">Loading...</td>
                                </tr>
                            </tbody>
                            <tbody v-if="data">
                                <tr v-for="student in data">
                                    <td>{{ student.id }}</td>
                                    <td>{{ student.firstname }}</td>
                                    <td>{{ student.lastname }}</td>
                                    <td>{{ student.email }}</td>
                                    <td>
                                        <RouterLink
                                            :to="{
                                                name: 'student-details',
                                                params: { username: student.username }
                                            }"
                                            >Display</RouterLink
                                        >
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <RouterLink
                        :to="{
                            name: 'student-new',
                            // params: { username: student.username }
                        }"
                        ><button class="newuser">Add new User</button>
                    </RouterLink>
                </div>
            </div>
            
        </div>
    </div>
</template>

<style src="/src/assets/students.css"></style>
