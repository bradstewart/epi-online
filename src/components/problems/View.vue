<template>
  <div class="main hbox space-between">
    <div class="flex-col flex-col-3">
      <div class="row-fluid" style="padding-bottom: 30px;">
        <h3 style="margin-top: 0;">{{ post.title }}</h3>
        <span class="label label-primary">Tag</span> <span class="label label-primary">Algorithms</span>
      </div>

      <h4>Instructions</h4>
      <p>{{{ post.problem }}}</p>
      <!-- TODO: Make this show only on click. -->
      <blockquote>
        <strong style="display: block;">Hint</strong> {{ post.hint }}
      </blockquote>
    </div>

    <div class="flex-col flex-col-5" style="background-color: #f5f5f5">
      <div class="row-fluid">

        <h4 style="font-size: 16px; font-weight: 500;">
          <i class="material-icons">mode_comment</i>
         Solution
       </h4>
        <div class="well" style="padding-left: 0">
          <ace-editor :content="post.skeleton"></ace-editor>
        </div>

        <h4 style="font-size: 16px; font-weight: 500;">
          <i class="material-icons">graphic_eq</i>
          Test Cases
        </h4>
        <div class="well" style="padding-left: 0">
          <ace-editor :content="post.test"></ace-editor>
        </div>

        <h4 style="font-size: 16px; font-weight: 500;">
          <i class="material-icons">message</i>
          Output
        </h4>
        <div class="well">
          <template v-if="result.tests">
            <log-output :buffer="output"></log-output>
          </template>
          <template v-else>
            Your output will appear here...
          </template>
        </div>
        <div class="row-fluid" style="margin: 10px; padding-top: 30px">
          <div class="pull-right">
            <modal :show.sync="isSubmitting">
              <p class="lead" style="margin: 0; text-align: center;">
                Submitting...
              </p>
              <load-bar></load-bar>
            </modal>
            <a @click.prevent="submit" class="btn btn-primary">Submit</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import _ from 'lodash'

  export default {

    data () {
      return {
        isSubmitting: false,
        post: {},
        result: {},
        output: [],
      }
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

    route: {
      data ({ next, to: { params: { id }}}) {
        next({
          post: this.fetchPost(id)
        })

        // Left over from collapsing menus in Materialize.
        // Just keeping this here in case we go back to that,
        // because I'll never remember this.
        //
        // this.$dispatch('open')
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

<style lang="less" scoped>
  @import "~assets/less/variables";

  // TODO: Use less variables for these colors.

  .well {
    background: #fff;
    margin: 0;
  }
  .accent-bg {
    background: #f5f5f5;
  }
  .material-icons,
  .fa {
    color: #0c7cd5;
    font-weight: 500;
  }
</style>
