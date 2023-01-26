<template>
  <div class="app">
    <div class="container">
      <h1>CREATE IMAGE</h1>
      <div>
        <div class="input-text">Describe Image</div>
        <textarea v-model="prompt" placeholder="Image description" v-on:click="resetError" />
        <div class="input-text">Select size</div>
        <select v-model="size" v-on:click="resetError">
          <option value="256x256">256x256</option>
          <option value="512x512">512x512</option>
          <option value="1024x1024">1024x1024</option>
        </select>
        <div>
          <button v-on:click="submitForm">Submit</button>
        </div>
      </div>
      <ErrorMessage :errorContent="errorContent" v-if="error" />
      <div v-if="imageCreated">
        <a :href="imageSrc" target="none" rel="__noopener">
          <img :src="imageSrc" alt="Generated Image" />
        </a>
      </div>
      <Spinner v-if="waitingResponse" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import Spinner from "../components/Spinner.vue"
import ErrorMessage from "../components/ErrorMessage.vue"

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
      waitingResponse: false,
      error: false,
      errorContent: "",
      prompt: "",
      size: "",
    };
  },
  methods: {
    async submitForm() {
      if (this.size === "" || this.prompt === "") {
        alert("Please select size and prompt");
      } else {
        this.waitingResponse = true
        this.imageCreated = false
        const imageInput: ImageGenerator = {
          prompt: this.prompt,
          size: this.size,
        };
        try {
          let response = await axios.post(
            "/api/generate-image", //"http://127.0.0.1:8000/api/generate-image",
            {
              prompt: imageInput.prompt,
              size: imageInput.size,
            }
          );
          this.waitingResponse = false
          const data = JSON.parse(response.data);
          if (data.success) {
            this.error = false;
            this.imageCreated = true;
            this.imageSrc = data.image;
            this.prompt = "";
            this.size = "";
          } else {
            this.error = true;
            this.imageCreated = false;
            this.errorContent = data.error;
          }
        } catch (error) {
          this.waitingResponse = false
          this.error = true;
          this.errorContent = error;
        }
      }
    },
    resetError(){
      this.error = false
      this.errorContent = "";
    }
  },
  components: {
  Spinner,
  ErrorMessage
}
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
</style>
