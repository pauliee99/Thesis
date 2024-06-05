<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useApplicationStore } from '@/stores/application.js';

const router = useRouter();
const { clearUserData, clearToken } = useApplicationStore();

const loading = ref(false);

const onFormSubmit = () => {
    // Perform a logout by flushing user data stored in tab state (pinia) and local storage (browser).
    // REMEMBER: authentication is stateless.
    // That is, if users store a valid JWT they can use it until is expired.
    // We cannot actually perform a logout because JWT cannot be invalided.
    // A solution is to blacklist the JWT until is expired.
    loading.value = true;
    clearUserData();
    clearToken();
    // setTimeout(function () {}, 2000); // Simulate a remote request.
    router.push({ name: 'login' }).then(() => {
        window.location.reload();
    });
};
</script>

<template>
    <div class="bg-body-tertiary">
        <div class="container">
            <div class="row py-4 px-3">
                <div class="col-4">
                    <div class="mb-4">
                        <h1 class="fs-3">Logout</h1>
                    </div>
                    <div class="spinner-border" role="status" v-if="loading">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <form v-else>
                        <div class="ring">
                            <i style="--clr:#00ff0a;"></i>
                            <i style="--clr:#ff0057;"></i>
                            <i style="--clr:#fffd44;"></i>
                            <button @click="onFormSubmit" type="submit" class="btn btn-primary">
                                Logout
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.ring {
  position: relative;
  width: 500px;
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.ring i {
  position: absolute;
  inset: 0;
  border: 2px solid #fff;
  transition: 0.5s;
}
.ring i:nth-child(1) {
  border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
  animation: animate 6s linear infinite;
}
.ring i:nth-child(2) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate 4s linear infinite;
}
.ring i:nth-child(3) {
  border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
  animation: animate2 10s linear infinite;
}
.ring:hover i {
  border: 6px solid var(--clr);
  filter: drop-shadow(0 0 20px var(--clr));
}
@keyframes animate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes animate2 {
  0% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(0deg);
  }
}
</style>
