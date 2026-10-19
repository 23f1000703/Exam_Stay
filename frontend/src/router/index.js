import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/StudentRegister.vue'),
    },
    {
      path: '/ownerregister',
      name: 'ownerregister',
      component: () => import('../views/OwnerRegister.vue'),
    },
    {
      path: '/admin',
      name: 'adminhome',
      component: () => import('../views/admin/AdminHome.vue'),
    },
    {
      path: '/owner/dashboard',
      name: 'ownerdashboard',
      component: () => import('../views/owner/HomeOwner.vue'),
    },
    {
      path: '/student',
      name: 'studenthome',
      component: () => import('../views/student/HomeStudent.vue'),
    },



    {
      path: '/admin/Students',
      name: 'adminstudents',
      component: () => import('../views/admin/AdminStudents.vue'),
    },
    {
      path: '/admin/students/:student_id',
      name: 'admin-student-detail',
      component: () => import('../views/admin/AdminStudentDetail.vue')
    },
    {
      path: '/admin/students/:student_id',
      name: 'admin-student-detail',
      component: () => import('../views/admin/AdminStudentDetail.vue')
    },
    {
      path: '/admin/properties',
      name: 'admin-properties',
      component: () => import('../views/admin/AdminOwnerproperties.vue')
    },
    {
      path: '/admin/properties/:property_id',
      name: 'admin-property-detail',
      component: () => import('../views/admin/AdminOwnerpropertydetail.vue')
    },
    {
      path: '/admin/bookings',
      name: 'admin-bookings',
      component: () => import('../views/admin/Adminuserbooking.vue')
    },
    {
      path: '/admin/verifications',
      name: 'admin-verifications',
      component: () => import('../views/admin/AdminVerification.vue')
    },
    {
      path: '/admin/complaints',
      name: 'admin-complaints',
      component: () => import('../views/admin/AdminComplaint.vue')
    },
    



    {
      path: '/owner/profile',
      name: 'owner-profile',
      component: () => import('../views/owner/OwnerProfile.vue')
    },
    {
    path: '/owner/properties/add',
    name: 'owner-add-property',
    component: () => import('../views/owner/AddProperty.vue'),
    },
    {
      path: '/owner/properties',
      name: 'ownerproperty',
      component: () => import('../views/owner/OwnerMyProperty.vue'),
    },
    {
      path: "/owner/properties/add-room",
      name: "AddRoom",
      component: () => import("../views/owner/AddRoom.vue"),
    },
    {
      path: "/owner/properties/:propertyId/amenities",
      name: "AddAmenities",
      component: () => import("../views/owner/AddAmenities.vue"),
    },
    {
      path: '/owner/properties/:property_id/images',
      name: 'owner-property-images',
      component: () => import('../views/owner/PropertyImage.vue'),
    },
    {
      path: '/owner/properties/:property_id',
      name: 'owner-property-view',
      component: () => import('../views/owner/OwnerPropertyView.vue')
   },
   {
      path: '/owner/bookings',
      name: 'owner-bookings',
      component: () => import('../views/owner/OwnerBooking.vue')
    },
    {
      path: '/owner/upcoming-bookings',
      name: 'owner-upcoming-bookings',
      component: () => import('../views/owner/UpcomingBookings.vue')
    },


    {
      path: '/student/properties',
      name: 'student-properties',
      component: () => import('../views/student/FindProperty.vue')
    },
    {
      path: '/student/profile',
      name: 'student-profile',
      component: () => import('../views/student/StudentProfile.vue')
    },
    {
      path: '/student/bookings',
      name: 'student-bookings',
      component: () => import('../views/student/BookingHistory.vue')
    },
    {
      path: '/student/properties/:id',
      name: 'StudentPropertyDetails',
      component: () => import('../views/student/StudentDetail.vue')
    }
  ],
})

export default router
