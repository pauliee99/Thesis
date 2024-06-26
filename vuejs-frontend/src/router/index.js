import { createRouter, createWebHistory } from 'vue-router';
// import HomeView from '../views/HomeView.vue';
import { useApplicationStore } from '@/stores/application.js';

// const { getUserData } = useApplicationStore();

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            // component: HomeView,
            component: () => import('../views/HomeView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/',
            name: 'home-manager',
            // component: HomeView,
            component: () => import('../views/HomeManagerView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/profile',
            name: 'profile',
            component: () => import('../views/ProfileView.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/profile/edit',
            name: 'editprofile',
            component: () => import('../views/EditProfileView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/profile/new-password',
            name: 'changepassword',
            component: () => import('../views/ChangePasswordView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/students',
            name: 'students',
            component: () => import('../views/StudentsView.vue'),
            meta: { requiresAuth: true, requiredRole: 'Admin' }
        },
        {
            path: '/students/new',
            name: 'student-new',
            component: () => import('../views/CreateUserView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/students/:username',
            name: 'student',
            component: () => import('../views/StudentView.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'student-details',
                    component: () => import('../views/StudentDetailsView.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'courses',
                    name: 'student-courses',
                    component: () => import('../views/StudentCoursesView.vue'),
                    meta: { requiresAuth: true }
                }
            ]
        },
        {
            path: '/event/:id',
            name: 'event',
            component: () => import('../views/EventView.vue'),
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    name: 'event-details',
                    component: () => import('../views/EventsDetailsView.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'edit',
                    name: 'edit-event-details',
                    component: () => import('../views/EditEventsDetailsView.vue'),
                    meta: { requiresAuth: true }
                },
                {
                    path: 'students',
                    name: 'course-students',
                    component: () => import('../views/CourseStudentsView.vue'),
                    meta: { requiresAuth: true }
                }
            ]
        },
        {
            path: '/event/new',
            name: 'event-new',
            component: () => import('../views/CreateEventView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/events',
            name: 'events',
            component: () => import('../views/EventsView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/logout',
            name: 'logout',
            component: () => import('../views/LogoutView.vue'),
            meta: { requiresAuth: true }
        }
    ]
});

router.beforeEach((to, from, next) => {
    const { isAuthenticated, getUserData, clearUserData } = useApplicationStore();
    // clearUserData() // if everything breaks again enable this once 
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    console.log(requiresAuth)
    if (requiresAuth && !isAuthenticated) {
        console.log('user not authenticated. redirecting to /login');
        next('/login');
    } else {
        const requiredRole = to.meta.requiredRole;
        const userRole = getUserData()?._value.role; // Get user role from state or local storage
        console.log("user tmp routers index idk ", requiredRole)
        if (requiresAuth && requiredRole) {
            if (userRole !== requiredRole){
                console.log("forbitten");
                // next('/forbidden'); // Redirect to forbidden page if role does not match
            } else {
                next(); 
            }
        } else {
            next(); // Continue navigation
        }
    }
});

export default router;
