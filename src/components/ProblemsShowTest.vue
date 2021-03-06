<template>
  <div class="page">

    <div class="row" style="margin: 12px;">
      <div :class="{ 'form-group': true, 'col-md-10': true, 'has-error': postInputError }">
        <input v-model="postInput" class="form-control" placeholder="Enter JSON...">
        <span class="help-block">{{ postInputError ? 'Invalid JSON!' : 'Pasting a test problem will render it below' }} </span>
      </div>
      <div class="col-md-2">
        <ui-button @click.prevent="postInput = null" color="primary" class="pull-right">
          clear
        </ui-button>
      </div>
    </div>
    <div class="page-content" style="height: calc(100% - 160px);">

      <div v-el:instructions class="split split-horizontal" style="overflow: auto">
        <div style="padding: 15px;">
          <div class="row-fluid" style="padding-bottom: 30px;">
            <h3 style="margin-top: 0;">{{ post.title }}</h3>
            <span class="label label-primary">Tag</span> <span class="label label-primary">Algorithms</span>
          </div>
          <div>{{{ post.problem }}}</div>
        </div>
      </div>

      <div v-el:solution class="split split-horizontal">
        <div v-el:solution-editor class="split">

          <panel title="Solution" body-padding="0">
            <div class="actions" slot="actions">
              <ui-select
                name="language"
                :value.sync="language"
                :options="languages"
                :default="language">
              </ui-select>
              <ui-select
                name="fontSize"
                :value.sync="fontSize"
                :options="fontSizes"
                :default="fontSize">
              </ui-select>
            </div>
            <ace-editor
              :mode="language.value"
              :font-size="fontSize.value"
              :content="post.skeleton">
            </ace-editor>
          </panel>
        </div>

        <div v-el:solution-results class="split" >
          <panel title="Output" icon="message">
            <template v-if="result.tests">
              <log-output :buffer="output"></log-output>
            </template>
            <span v-else>
              Your output will appear here...
            </span>
          </panel>
        </div>
      </div>
    </div>

    <div class="page-footer">

      <div class="pull-right">
        <div class="actions">
        <ui-button data-toggle="button" v-popover.left="post.hint" flat icon-left icon="help" color="default">
          HINT
        </ui-button>

        <ui-button @click.prevent="submit" raised icon-left icon="send" color="primary">
          Submit
        </ui-button>
      </div>
      <modal :show.sync="isSubmitting">
        <p class="lead" style="margin: 0; text-align: center;">
          Submitting...
        </p>
        <load-bar></load-bar>
      </modal>

    </div>


  </div>
</template>

<script>
  import Split from 'split.js'
  import _ from 'lodash'

  const LANGUAGES = [{
    text: 'Java',
    value: 'java',
  }, {
    text: 'C/C++',
    value: 'c_cpp',
  }]

  const FONT_SIZES = [{
    text: '12px',
    value: '12px',
  }, {
    text: '14px',
    value: '14px',
  }]

  export default {

    data () {
      return {
        isSubmitting: false,
        showHint: false,
        language: LANGUAGES[0],
        fontSize: FONT_SIZES[0],
        postInput: '',
        postInputError: false,
        post: {},
        result: {},
        output: [],
      }
    },

    computed: {
      languages () {
        return LANGUAGES
      },
      fontSizes () {
        return FONT_SIZES
      },
    },

    watch: {
      postInput (newVal) {
        if (newVal && _.isString(newVal)) {
          try {
            let parsed = JSON.parse(newVal)
            this.post = parsed
            this.postInputError = false
          } catch (err) {
            this.postInputError = true
          }
        } else {
          this.post = {}
          this.postInputError = false
        }
      },
    },

    methods: {
      log (...data) {
        this.output.push(...data)
      },
      fetchPost (id) {
        return this.$http
          .get({ url: `/static/data/posts/${id}.json`})
          .then((res) => res.data)
          .catch((err) => console.error(err))
      },
      reset () {
        if (confirm('Reset?')) {
          this.fetchPost(this.$route.params.id).then((post) => {
            this.post = post
          })
        }
      },
      submit () {
        this.isSubmitting = true
        this.log(`<strong>Submission started @ ${new Date().toISOString()}</strong><br />`)

        // Add some "async"
        setTimeout(() => {
          return this.$http
            .get({ url: `/static/data/result.json`})
            .then((res) => {
              this.result = res.data

              let passed = 0
              res.data.tests.forEach((test) => {
                if (test.status === 'ok') {
                  passed++
                }
                // TODO: Format failures differently (display inputs).
                // TODO: Display check mark when all passing.

                this.output.push(
                  `    ${test.status}\t${_.padEnd(test.description, 25)}\t--\tExpected: ${test.expected_output} \t Actual: ${test.user_output}`
                )
              })

              this.log(`<strong>Passed ${passed}/${res.data.tests.length}</strong><br /><br />`)
              this.isSubmitting = false
            })
            .catch((err) => {
              this.isSubmitting = false
              console.error(err)
            })
          }, Math.round(Math.random()*1500) + 500)
      }
    },

    ready () {
      Split([this.$els.instructions, this.$els.solution], {
        sizes: [40, 60],
        minSize: 100,
        // direction: 'vertical'
      })

      setTimeout(() => {
        Split([this.$els.solutionEditor, this.$els.solutionResults], {
          sizes: [70, 30],
          // minSize: 100,
          // gutterSize: 2,
          direction: 'vertical'
        })
      })


    },

    // route: {
    //   data ({ next, to: { params: { id }}}) {
    //     next({
    //       post: this.fetchPost(id)
    //     })
    //
    //     // Left over from collapsing menus in Materialize.
    //     // Just keeping this here in case we go back to that,
    //     // because I'll never remember this.
    //     //
    //     // this.$dispatch('open')
    //   },
    // },
  }
</script>

<style lang="less">
  @import "~assets/less/variables";

  .ace_content {
    background: #fff !important;
  }
  .ace_gutter {
    background: #fff !important;
  }
</style>

<style lang="less">
  @import "~assets/less/variables";


  .ui-toolbar.ui-toolbar-sm {
    .ui-icon-button {
      width: 32px;
      height: 32px;

      .ui-icon {
        font-size: 20px;
      }
    }
  }
  .actions {
    a,
    div.ui-select {
      margin: 0 8px;

      &:last-child {
        margin-right: 0;
      }
      &:first-child {
        margin-left: 0;
      }
    }
  }

  .page {
    height: 100%;
    background-color: #eee;
    padding: 8px;

    .page-content {
      // height: calc(~"100% - 45px"); // .page-footer height! + TEST INPUT HEIGHT
    }

    .page-footer {
      height: 45px;
      padding: 8px 0 0 0;
    }
  }

  .split {
    box-sizing: border-box;
    background-color: #fff;
    overflow-x: hidden;
    overflow-y: hidden;

    &.split-horizontal {
      height: 100%;
      float: left;
    }
  }

  .gutter {
    background-color: #eee;
    background-repeat: no-repeat;
    background-position: 50%;

    &.gutter-horizontal {
      background-image: url('~split.js/grips/vertical.png');
      cursor: col-resize;
      height: 100%;
      float: left;
    }

    &.gutter-vertical {
      background-image: url('~split.js/grips/horizontal.png');
      cursor: row-resize;
    }
  }
</style>
