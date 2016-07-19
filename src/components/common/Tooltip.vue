<template>
  <span v-el:tooltip class="tooltipped"
    :data-position="position"
    data-delay="50"
    :data-title="content">
    <slot></slot>
  </span>
</template>

<script>
  export default {
    props: {
      content: {
        type: String,
        default: 'Tooltip',
      },
      position: {
        type: String,
        default: 'bottom',
      },
    },

    ready () {
      $(this.$els.tooltip).tooltip()
      console.log('TOOOLTIPPP')
    }
  }
</script>
