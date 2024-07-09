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
const urlRef1 = computed(() => {
    return 'http://localhost:8000/users/' + studentIdRef.value;
});
const authRef1 = ref(false); //@TODO: na to kamo true molis vao je to auth tou backend
const { data, loading, performRequest:performRequest1 } = useRemoteData(urlRef1, authRef1);

onMounted(() => {
    studentIdRef.value = route.params.username;
    performRequest1({ token }) //@TODO: na valo to token molis saso to authendication tou endpoint
});

const formDataRef = ref({
    id: data.id,
    firstname: data.firstname,
    lastname: data.lastname,
    email: data.email,
    username: data.username,
    birth_date: data.birth_date,
    profile_picture: data.profile_picture,
    student_id: data.student_id,
    disabled: data.disabled,
});
const userIdRef = ref(null);
const urlRef2 = computed(() => {
    return 'http://localhost:8000/users/' + userIdRef.value;
});
const authRef2 = ref(true);
const methodRef = ref('PUT');
const showpopup = ref(false);

const { performRequest:performRequest2 } = useRemoteData(urlRef2, authRef2, methodRef, formDataRef);
const onSubmit = () => {
    userIdRef.value = data.value.id;
    formDataRef.value.id = data.value.id;
    formDataRef.value.firstname = data.value.firstname;
    formDataRef.value.lastname = data.value.lastname;
    formDataRef.value.email = data.value.email;
    formDataRef.value.username = data.value.username;
    formDataRef.value.birth_date = data.value.birth_date;
    formDataRef.value.profile_picture = data.value.profile_picture.split('/').pop().split('?')[0];
    formDataRef.value.student_id = data.value.student_id;
    formDataRef.value.disabled = false;
    console.log("formDataRef", formDataRef);
    console.log("formDataRef.value", formDataRef.value);
    console.log("userIdRef.value", userIdRef.value);
    console.log("data.id", data.id);
    performRequest2({ token })
};
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
                    <th>ID</th>
                    <td>{{ data.id }}</td>
                </tr>
                <tr>
                    <th>First Name</th>
                    <td><input class="form-control" id="usreditfname" v-model="data.firstname" type="text"/></td>
                </tr>
                <tr>
                    <th>Last Name</th>
                    <td><input class="form-control" id="usereditlname" v-model="data.lastname" type="text"/></td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td><input class="form-control" id="usereditemail" v-model="data.email" type="email"/></td>
                </tr>
                <tr>
                    <th>Birth Date</th>
                    <td><input class="form-control" id="usereditbday" v-model="data.birth_date" type="text"/></td>
                </tr>
                <tr v-if="data.role === 'Student'">
                    <th>Student ID</th>
                    <td><input class="form-control" id="usereditstid" v-model="data.student_id" type="text"/></td>
                </tr>
                <tr>
                    <th>Role</th>
                    <td>{{ data.role }}</td>
                    <!-- <td><input class="form-control" id="usereditrole" v-model="data.role" type="text"/></td> -->
                </tr>
                <tr v-if="false">
                    <th>Profile Picture</th>
                    <td><input class="form-control" v-model="data.profile_picture" type="text"/></td>
                </tr>
                <tr>
                    <th>Action</th>
                    <td><RouterLink
                        class="nav-link"
                        :to="{ name: 'student-details', params: { id: studentIdRef } }"
                        ><button class="btn btn-primary" @click="onSubmit" type="button">Update Record</button></RouterLink
                    ></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
