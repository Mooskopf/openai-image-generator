<template>
  <div class="app">
    <div class="container">
      <h1>CREATE IMAGE</h1>
      <form v-on:submit="submitForm">
        <div class="input-text">Describe Image</div>
        <textarea required placeholder="Image description" name="prompt" />
        <div class="input-text">Select size</div>
        <select name="size">
          <option value="256x256">256x256</option>
          <option value="512x512">512x512</option>
          <option value="1024x1024">1024x1024</option>
        </select>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
      <div v-if="error">
        <div class="error" v-html="errorContent" />
      </div>
      <div v-if="imageCreated">
        <a :href="imageSrc" target="none" rel="__noopener">
          <img :src="imageSrc" alt="Generated Image" />
        </a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

interface ImageGenerator {
  prompt: string;
  size: string;
}

export default Vue.extend({
  name: "IndexPage",
  data() {
    return {
      imageSrc: "",
      imageCreated: false,
      error: false,
      errorContent: "",
    };
  },
  methods: {
    async submitForm(e: any) {
      e.preventDefault();
      const imageInput: ImageGenerator = {
        prompt: e.target.prompt.value,
        size: e.target.size.value,
      };
      try {
        let response = await axios.post(
          "/api/generate-image",   //"http://127.0.0.1:8000/generate-image",
          {
            prompt: imageInput.prompt,
            size: imageInput.size,
          }
        );
        const data = JSON.parse(response.data)
        if (data.success) {
          this.error = false
          this.imageCreated = true
          this.imageSrc = data.image
        } else {
          this.error = true
          this.imageCreated = false
          this.errorContent = data.error
        }
      } catch (error) {
        this.error = true
        this.errorContent = error
      }
    },
  },
});
</script>

<style>
body {
  margin: 0;
}

.app {
  background-color: black;
  min-height: 100vh;
}

.container {
  width: 80%;
  margin: 0 auto;
  padding-top: 100px;
  color: white;
  user-select: none;
}

.container h1 {
  margin-bottom: 60px;
}

.input-text {
  font-size: 28px;
  margin-bottom: 20px;
  margin-top: 30px;
}

.container textarea {
  width: 300px;
  padding-left: 10px;
  padding-top: 10px;
  outline: none;
}

.container select {
  height: 24px;
  margin-bottom: 20px;
}

.container button {
  margin-top: 20px;
  padding: 10px 20px 10px 20px;
  font-size: 18px;
  font-weight: bold;
}

.container button:hover {
  cursor: pointer;
}

.container img {
  margin-top: 100px;
  margin-bottom: 100px;
}

.error {
  margin-top: 60px;
  color: red;
}
</style>
