<template>
  <div v-el:editor :style="editorStyle"></div>
</template>

<script>
  /* global ace */

  // TODO: Make Language and Font-size configurable.
  // 
  export default {
    props: {
      content: {
        type: String,
        default: '',
      },
      height: {
        type: Number,
        default: 300,
      },
      mode: {
        type: String,
        default: 'java',
      },
      theme: {
        type: String,
        default: 'github',
      },
    },

    data () {
      return {
        editorIsUpdating: false,
      }
    },

    watch: {
      content (newValue, oldValue) {
        if (!this.editorIsUpdating) {
          this.editor.setValue(newValue, -1)
        }
      },
    },

    computed: {
      editorStyle () {
        return {
          height: `${this.height}px`,
        }
      },
    },

    methods: {
      editorChanged (event) {
        this.editorIsUpdating = true
        this.content = this.editor.getValue()
        this.$nextTick(() => this.editorIsUpdating = false)
      },
    },

    ready () {
      //TODO: Validate mode and theme strings.

      let e = ace.edit(this.$els.editor)
          e.getSession().setMode(`ace/mode/${this.mode}`)
          e.setTheme(`ace/theme/${this.theme}`)
          e.setShowPrintMargin(false)
          e.$blockScrolling = Infinity
          e.setValue(this.content, 1)
          e.setOptions({
            autoScrollEditorIntoView: true,
            maxLines: 15,
            minLines: 8,
          })

      this.editor = e

      this.editor.getSession().on('change', this.editorChanged)
    },

    beforeDestroy () {
      this.editor.destroy()
    },

  }
</script>

<style lang="less" scoped>

</style>
