<template>
  <div id="app">
    <app-header></app-header>
    <div id="content-container">
      <div id="content">
        <router-view></router-view>
      </div>
    </div>
    <app-footer></app-footer>
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
  // General Layout
  ///

  html,
  body,
  #app {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
  }

  header,
  footer {
    width: 100%;
    position: fixed;
  }

  header {
    height: @header-height;
    top: 0;
  }

  footer {
    height: @footer-height;
    bottom: 0;
  }

  #content-container {
    height: 100vh;
    margin: 0 auto;
    padding: @header-height 0 @footer-height 0;
    overflow: hidden;
  }

  #content {
    overflow-y: auto;
    height: 100%;
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
