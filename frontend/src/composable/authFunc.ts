import { API_URL } from '@/config'
import { ref } from 'vue';
import axios from 'axios';
import { signupconffunc } from './signupconf';
import { generateUsernameFunc } from './generateUsername';
import { openModalLogin } from './openmodalLogin'
import { useAuthStore } from '../stores/authstore';
import { useRouter } from 'vue-router';

import { setTokens } from '@/composable/http'

const { opensignupconf } = signupconffunc();
const { username } = generateUsernameFunc();
const { closeModal } = openModalLogin();
const loggingInLoading = ref<boolean>(false);
const signupLoading = ref<boolean>(false);



const email = ref<string>('');
const password = ref<string>('');
const confirmPassword = ref<string>('');
const firstName = ref<string>('');
const lastName = ref<string>('');
const success = ref<boolean>(false);
const signupError = ref<string>('');
const loginError = ref<string>('');

type signupResponse = {
  password: string;
  email: string;
  username: string;
  confirmPassword: string;
  firstName: string;
  lastName: string;
  success: boolean;
};

const resetForm = () => {
  email.value = '';
  password.value = '';
  confirmPassword.value = '';
  firstName.value = '';
  lastName.value = '';
  username.value = '';
};


export function authFunc() {

const route = useRouter();
  
const submitLoginForm = async () => {
  
  loggingInLoading.value = true;
  
  loginError.value = '';
  
  const authStore = useAuthStore();

  try {

    const res = await axios.post(
      `${API_URL}/api/login`,
      {
        email: email.value,
        password: password.value,
      }
    );

    console.log(res.data);

    authStore.setAccessToken(res.data.access_token);
    authStore.setUser(res.data.user);

    closeModal()
    await authStore.fetchProfile();
    setTokens(res.data.access_token, res.data.refresh_token)
    route.push('/dash');

  } catch (err: any) {

    loginError.value = err.response?.data?.detail || 'Something went wrong';

    setTimeout(() => {
      loginError.value = '';
    }, 3000);

  }finally{
    loggingInLoading.value = false;
  }
};

const submitSignupForm = async () => {
  signupLoading.value = true;
  signupError.value = '';

  try {
    const res = await axios.post<signupResponse>(`${API_URL}/api/signup`, {
      email: email.value,
      password: password.value,
      username: username.value,
      confirmPassword: confirmPassword.value,
      firstName: firstName.value,
      lastName: lastName.value,
      success: success.value,
    });

    if (res.data.success) {
      resetForm();
      opensignupconf();
    }
  } catch (err: any) {
    console.log("error: ", err.response?.data?.detail)
    signupError.value = err.response?.data?.detail || 'Something went wrong';


    setTimeout(() => {
      signupError.value = '';
    }, 3000);
  } finally {
    signupLoading.value = false;
  }
};
  
  return {
    email,
    password,
    confirmPassword,
    firstName,
    lastName,
    loggingInLoading,
    signupLoading,
    signupError,
    loginError,
    submitLoginForm,
    submitSignupForm
  };
}
