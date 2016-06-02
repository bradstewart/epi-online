<template>
  <div class="vbox viewport">
    <app-header></app-header>
    <section class="main hbox" style="justify-content: space-around">
      <router-view></router-view>
    </section>
    <!-- <app-footer></app-footer> -->
  </div>
</template>

<script>
  import AppHeader from './components/app/AppHeader'
  import AppFooter from './components/app/AppFooter'

  export default {
    components: {
      AppHeader,
      AppFooter,
    }
  }
</script>

<style lang="less">
  @import "assets/less/main";

  ///
  // Flexbox layout stuff.
  ////

  /*
    Force full width & height.

    If this block is removed, the layout height/length will be determined by
    the amount of content in the page. That might result in a page which has
    a footer only a few inches from the top of the viewport, or one which
    scrolls beyond the viewport.

    This forces the layout to always be full screen regardless of how much,
    or how little, content is in place. Neither is "right" or "wrong", there
    are valid cases for each. I just want to be clear what's controlling the
    page/viewport height.
  */
  html,
  body,
  #app,
  .viewport {
    width: 100%;
    height: 100%;
    margin: 0;
  }

  /* items flex/expand vertically */
  .vbox {
    display: flex;
    flex-direction: column;
  }

  /* items flex/expand horizontally */
  .hbox {
    display: flex;
    flex-direction: row;
  }

  .space-between {
    justify-content: space-between;
  }

  /* I went with a fixed height header & footer because it's a common case.
    This could easily be altered to flex proportionally with the page.
  */
  header, footer {
    height: 65px;
  }

  footer {
    // border-top: 1px solid @gray;
    // background-color: @brand-primary;
    // background-color: #f5f5f5;
    // z-index: 33300303000;
    // box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    // border: 1px solid #eee;
    p {
      line-height: 65px !important;
      color: #fff;
      margin: 0;
    }
    .actions {
      margin: 13.5px 0;
      a {
        height: 35px;
        cursor: pointer;
      }
    }
  }

  .main {
    flex: 1;
  }

  .flex-col-3 {
    flex: 5;
  }

  .flex-col-5 {
    flex: 7;
  }

  .flex-col {
    padding: 2rem;
    overflow: auto;
  }

  ////
  // Global Styles
  ////

  .container {
    position: relative;
    min-height: 100%;
    width: 100%;
    max-width: 100%;
    padding: 0 2rem;
  }

  pre {
    border: none;
    margin: 0;
    padding: 0;
    background: transparent;
    font-size: 10px;
  }

  .material-icons {
    vertical-align: middle;
  }
</style>
