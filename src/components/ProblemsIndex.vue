<template>
  <div style="flex: 1; margin: 0 50px;">
    <div class="page-header">
      <h1>Problems <small>WIP</small></h1>
    </div>
    <div v-for="group in groups" style="display: block">
      <h4> {{group.title}}</h4>
    <div class="list-group">
      <a
        v-for="post in group.posts"
        v-link="{ name: 'problem', params: { group: group.id, id: post.slug }}"
        class="list-group-item">
        {{ post.title }}
      </a>
    </div>
  </div>
</div>
</template>

<script>
  export default {
    data () {
      return {
        groups: [],
      }
    },

    route: {
      activate ({ next, to: { params: { group, id }} }) {
        return this.$http
          .get({ url: '/static/data/posts.json'})
          .then((res) => this.groups = res.data)
          .catch(err => console.error(err))
      },
    },
  }
</script>
