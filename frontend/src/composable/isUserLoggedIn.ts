import { ref } from 'vue';

const isUserLoggedin = ref(!!localStorage.getItem('access_token'));

export function isuserloggedinFunc() {
  return {
    isUserLoggedin
  };
}