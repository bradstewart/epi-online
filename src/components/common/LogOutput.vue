<template>
  <div class="log">
    <div v-el:output :style="computedStyle">
      <pre v-for="line in buffer" track-by="$index">{{{ line }}}</pre>
    </div>
  </div>
</template>

<script>
  // import _ from 'lodash'

  export default {
    props: {
      buffer: {
        type: Array,
        required: true,
      },

      height: {
        type: Number,
        default: 200,
      }
    },

    // data () {
    //   return {
    //     buffer: [],
    //   }
    // },

    computed: {
      computedStyle () {
        return {
          'overflow': 'auto',
          'margin-right': '-20px',
          'height': `${this.height}px`,
          'max-height': `${this.height}px`,
        }
      },
    },

    watch: {
      buffer (newValue) {
        this.scrollBottom()
      },
    },

    methods: {
      scrollBottom () {
        this.$els.output.scrollTop = this.$els.output.scrollHeight
      }
    },

    ready () {
      // this.buffer.push('Waiting for input...')
    }

  }
</script>

<style lang="less" scoped>
.log {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'source-code-pro', monospace;
}
  pre {
    display: block;
  }
</style>
