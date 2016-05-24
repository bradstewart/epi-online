<template>
  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p>Place sticky footer content here.</p>
        </div>
        <div class="col-md-6 actions">
          <div class="pull-right">
            <!-- <a @click.prevent="reset" class="btn btn-default">Reset</a> -->
            <!-- <a @click.prevent="runTests" class="btn btn-default">Run Tests</a> -->
            <!-- <a  class="btn btn-default">Reset</a> -->
          </div>
        </div>
      </div>
    </div>
  </footer>
<script>
  export default {

  }
</script>

<style lang="less" scoped>
  @import "assets/less/variables";


  // .footer {
  //   p,
  //   span,
  //   strong {
  //     line-height: 60px;
  //   }
  // }
  .actions {
    margin: 13.5px 0;
    a {
      height: 35px;
      cursor: pointer;
    }
  }
</style>
