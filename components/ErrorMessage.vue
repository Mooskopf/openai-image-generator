.<template>
    <div class="error">{{errorContent}}</div>
</template>

<script>
export default {
    name:"ErrorMessage",
    props: ["errorContent"]
};
</script>

<style scoped>
.error {
  margin-top: 100px;
  color: red;
}
</style>