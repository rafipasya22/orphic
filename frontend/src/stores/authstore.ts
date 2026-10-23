import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { logoutconffunc } from '../composable/logoutconf';

type Profile = {
  username: string;
  first_name: string;
  last_name: string;
  profile_picture_url: string | null;
};

export const useAuthStore = defineStore('auth', () => {

  const router = useRouter();
  const { closelogoutconf } = logoutconffunc();

  const user = ref<any | null>(
    JSON.parse(localStorage.getItem('user') || 'null')
  );

  const profile = ref<Profile | null>(null);

  const accessToken = ref<string | null>(
    localStorage.getItem('access_token')
  );

  const setUser = (newUser: any) => {

    user.value = newUser;

    localStorage.setItem(
      'user',
      JSON.stringify(newUser)
    );
  };

  const setAccessToken = (token: string) => {

    accessToken.value = token;

    localStorage.setItem(
      'access_token',
      token
    );
  };

  const fetchProfile = async () => {

    if (!user.value?.id) return;

    try {

      const res = await axios.get(
        `http://localhost:8000/api/profile/${user.value.id}`
      );

      profile.value = res.data;

    } catch (err) {

      console.log(err);

    }
  };

  const logout = async () => {

    localStorage.removeItem('access_token');
    localStorage.removeItem('user');

    user.value = null;
    profile.value = null;
    accessToken.value = null;

    router.replace('/');
  };

  return {
    user,
    profile,
    accessToken,
    setUser,
    setAccessToken,
    fetchProfile,
    logout
  };

});