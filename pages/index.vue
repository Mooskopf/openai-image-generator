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
      <div v-if="error">
        <div class="error" v-html="errorContent" />
      </div>
      <div v-if="imageCreated">
        <a :href="imageSrc" target="none" rel="__noopener">
          <img :src="imageSrc" alt="Generated Image" />
        </a>
      </div>
      <div v-if="waitingResponse" class="lds-spinner">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
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
  margin-top: 100px;
  color: red;
}

.lds-spinner {
  margin-top: 100px;
  width: 80px;
  height: 80px;
}
.lds-spinner div {
  transform-origin: 40px 40px;
  animation: lds-spinner 1.2s linear infinite;
}
.lds-spinner div:after {
  content: " ";
  display: block;
  position: absolute;
  top: 3px;
  left: 37px;
  width: 6px;
  height: 18px;
  border-radius: 20%;
  background: #fff;
}
.lds-spinner div:nth-child(1) {
  transform: rotate(0deg);
  animation-delay: -1.1s;
}
.lds-spinner div:nth-child(2) {
  transform: rotate(30deg);
  animation-delay: -1s;
}
.lds-spinner div:nth-child(3) {
  transform: rotate(60deg);
  animation-delay: -0.9s;
}
.lds-spinner div:nth-child(4) {
  transform: rotate(90deg);
  animation-delay: -0.8s;
}
.lds-spinner div:nth-child(5) {
  transform: rotate(120deg);
  animation-delay: -0.7s;
}
.lds-spinner div:nth-child(6) {
  transform: rotate(150deg);
  animation-delay: -0.6s;
}
.lds-spinner div:nth-child(7) {
  transform: rotate(180deg);
  animation-delay: -0.5s;
}
.lds-spinner div:nth-child(8) {
  transform: rotate(210deg);
  animation-delay: -0.4s;
}
.lds-spinner div:nth-child(9) {
  transform: rotate(240deg);
  animation-delay: -0.3s;
}
.lds-spinner div:nth-child(10) {
  transform: rotate(270deg);
  animation-delay: -0.2s;
}
.lds-spinner div:nth-child(11) {
  transform: rotate(300deg);
  animation-delay: -0.1s;
}
.lds-spinner div:nth-child(12) {
  transform: rotate(330deg);
  animation-delay: 0s;
}
@keyframes lds-spinner {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

</style>
