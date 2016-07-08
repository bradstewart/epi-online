<template>
  <div>
    <div v-el:editor :style="editorStyle"></div>
  </div>

</template>

<script>
  /* global ace */

  const MODES = {
    'java': true,
    'c_cpp': true,
  }

  // TODO: Make Language and Font-size configurable.
  //
  export default {
    props: {
      content: {
        type: String,
        default: '',
      },
      mode: {
        type: String,
        default: 'java',
        validator: (val) => MODES[val],
      },
      theme: {
        type: String,
        default: 'github',
      },
      fontSize: {
        type: String,
        default: '12px',
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

      mode (newValue) {
        this.editor.getSession().setMode(`ace/mode/${newValue}`)
      },
    },

    computed: {
      editorStyle () {
        return {
          'font-size': this.fontSize,
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
            maxLines: Infinity,
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
