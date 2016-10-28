<template>
  <div class="page">
    <div class="page-content">
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
              :mode="language.aceEditorId"
              :font-size="fontSize"
              :content.sync="code.skeleton">
            </ace-editor>
          </panel>
        </div>

        <div v-el:solution-results class="split">
          <panel title="Output" icon="message">
            <template v-if="output.length">
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
          <ui-button
            v-popover.left="post.hint"
            type="flat"
            icon-left
            icon="help"
            color="default"
            text="Hint">
          </ui-button>
          <ui-button
            @click.prevent="isConfirmingReset = true"
            type="flat"
            icon-left
            icon="autorenew"
            color="default"
            text="Reset">
          </ui-button>
          <ui-button
            @click.prevent="submit"
            :loading="isSubmitting"
            raised
            icon-left
            icon="send"
            color="primary"
            text="Submit">
          </ui-button>
        </div>

        <ui-confirm
          :show.sync="isConfirmingReset"
          header="Reset Problem"
          close-on-confirm
          @confirmed="reset">
          All changes will be lost. Are you sure?
        </ui-confirm>

        <ui-modal
          :show.sync="isSubmitting"
          header="Submitting..."
          type="small"
          hide-footer
          :dismissible="false"
          :show-close-button="false">
          <ui-preloader show></ui-preloader>
        </ui-modal>
      </div>

    </div>
  </div>
</template>

<script>
  import Split from 'split.js'
  import _ from 'lodash'
  import * as languages from 'src/languages'
  import { fontSizes } from 'src/editorOptions'

  export default {
    data () {
      return {
        isConfirmingReset: false,
        isSubmitting: false,
        showHint: false,
        language: languages.Java,
        fontSize: fontSizes[0],
        post: {},
        output: [],
      }
    },

    computed: {
      languages () {
        return _.values(languages)
      },
      fontSizes () {
        return fontSizes
      },
      code () {
        return _.get(this.post, ['code', this.language.value], {})
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
        this.isConfirmingReset = false

        this.fetchPost(this.$route.params.id).then((post) => {
          this.post = post
        })
      },

      submit () {
        this.isSubmitting = true
        this.log(`<strong>Submission started @ ${new Date().toISOString()}</strong><br />`)

        return this
          .$http
          .post({
            url: 'http://epijudge.ddns.net:3000/compile',
            data: JSON.stringify({
              filename: this.code.filename,
              language: this.language.compileBoxId,
              code: this.language.assemble(this.code),
              // TODO: Do we need this/what should it's value be?
              stdIn: 'TODO',
            }),
            method: 'POST',
          })
          .then((response) => {
            this._handleResponse(response)
            this.isSubmitting = false
          })
          .catch((err) => {
            this.isSubmitting = false
            console.error(err)
          })

        // Add some "async"
        // setTimeout(() => {
        //   return this.$http
        //     .get({ url: `/static/data/result.json`})
        //     .then((response) => {
        //       this._handleResponse(response)
        //       this.isSubmitting = false
        //     })
        //     .catch((err) => {
        //       this.isSubmitting = false
        //       console.error(err)
        //     })
        //   }, Math.round(Math.random()*1500) + 500)
      },

      _handleResponse (response) {
        let { output, errors, test } = response.data

        this.log(output)

        if (errors) return this.log(errors)

        let passed = 0

        tests.forEach((test) => {
          if (test.status === 'ok') passed++

          // TODO: Format failures differently (display inputs).
          // TODO: Display check mark when all passing.

          this.log(
            `    ${test.status}\t${_.padEnd(test.description, 25)}\t--\tExpected: ${test.expected_output} \t Actual: ${test.user_output}`
          )
        })

        this.log(`<strong>Passed ${passed}/${tests.length}</strong><br /><br />`)
      },

      _initDraggablePanels () {
        Split([this.$els.instructions, this.$els.solution], {
          sizes: [40, 60],
          minSize: 100,
        })

        setTimeout(() => {
          Split([this.$els.solutionEditor, this.$els.solutionResults], {
            sizes: [70, 30],
            direction: 'vertical'
          })
        })
      },
    },

    ready () {
      this._initDraggablePanels()
    },

    route: {
      data ({ next, to: { params: { id }}}) {
        next({
          post: this.fetchPost(id)
        })
      },
    },
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
      height: calc(~"100% - 45px"); // .page-footer height!
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
