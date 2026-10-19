<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router'
    import { useAuthStore } from '../stores/auth'

    const router = useRouter()
    const authStore = useAuthStore()

    const email = ref('');
    const password = ref('');

    const passwordError = ref('')
    

    const validatePassword = () => {
        if (password.value.length < 8){
            passwordError.value ='Your password length must be 8'
            return false
        } 
        else {
            passwordError.value = '';
            return true
        }

    }

    async function login(){
        if (!validatePassword()){
            alert("Invalid password length");
            return
        }
        if (email.value == ""|| password.value == ""){
            alert("please fill Email and Password")
            return
        }

        const user = {
            email : email.value,
            password : password.value
        }

        const response = await fetch('http://127.0.0.1:5000/api/login',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });
        console.log(response)

        

        if (!response.ok){
            const errordata = await response.json();
            console.error(errordata)
            alert(`Login failed: ${errordata.message}`);
            return;
        }
        else{
            const data = await response.json();
            console.log(data)
            
            
            // localStorage.removeItem('token')
            alert(data.message)


            const role = data.user_details.roles[0] 

            console.log('Token received:',Boolean(data.user_details?.auth_token))

           console.log('User details:', data.user_details)

            authStore.login(
                  data.user_details.auth_token,
                  role,
                  data.user_details.user_id
              )
            console.log('API TOKEN:', data.user_details.auth_token)
            console.log('PINIA TOKEN:', authStore.token)

            if (role === 'admin') {
            router.push('/admin')
            }
            else if (role === 'customer') {
                router.push('/student')
            }
            else if (role ==='owner'){
                router.push('/owner/dashboard')
            }
            else{
                console.log("invalid role")
            }
            
            }

        } 
    

</script>

<template>
  <div class="login-page">

    <div class="login-card">

      <div class="login-header">
        <p class="label">WELCOME BACK</p>

        <h1>Login to ExamStay</h1>

        <p>
          Access your account to manage your stays and bookings.
        </p>
      </div>

      <form @submit.prevent="login">

        <div class="form-group">
          <label for="email">Email</label>

          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>

          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <div class="form-options">
          <label class="remember">
            <input
              v-model="rememberMe"
              type="checkbox"
            />
            Remember me
          </label>

          <a href="#">Forgot password?</a>
        </div>

        <button type="submit">
          Login
        </button>

      </form>

      <div class="register-link">
        <p>
          Don't have an account?
          <RouterLink to="/register">
            Create an account
          </RouterLink>
        </p>
      </div>

    </div>

  </div>
</template>


<style scoped>
.login-page {
  min-height: calc(100vh - 70px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  background: #f7f7f5;
}

.login-card {
  width: 100%;
  max-width: 440px;
  padding: 40px;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #666;
  margin-bottom: 12px;
}

.login-header h1 {
  font-size: 30px;
  margin-bottom: 12px;
}

.login-header p:last-child {
  color: #666;
  line-height: 1.5;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
}

.form-group input[type="email"],
.form-group input[type="password"] {
  width: 100%;
  padding: 13px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  outline: none;
}

.form-group input:focus {
  border-color: #222;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.remember {
  display: flex;
  align-items: center;
  gap: 7px;
}

.form-options a {
  color: #222;
  text-decoration: none;
}

button {
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 6px;
  background: #171717;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.register-link {
  margin-top: 25px;
  text-align: center;
  font-size: 14px;
}

.register-link p {
  color: #666;
}

.register-link a {
  color: #171717;
  font-weight: 600;
  text-decoration: none;
}
</style>