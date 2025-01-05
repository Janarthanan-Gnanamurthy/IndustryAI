<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->

    <div >
      <nav class="bg-blue-600 p-5 ">
        <RouterLink to="/" class="btn mr-5">Home</RouterLink>
        <RouterLink to="/about" class="btn">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
