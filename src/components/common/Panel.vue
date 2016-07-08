<template>
  <div class="panel panel-flat">
    <ui-toolbar class="ui-toolbar-sm" flat hide-nav-icon  type="clear">
      <h5 style="padding-left: 15px;">{{ title }}</h5>
      <!-- <ui-icon icon="assessment"></ui-icon> Solution -->
        <div slot="actions" style="padding-right: 15px">


          <slot name="actions">
          </slot>
          </div>
      </ui-toolbar>
    <!-- <div class="panel-heading">
      <h5 >{{ title }}</h5>

      <div v-if="actions" class="panel-actions">
        <div >
          <a  v-for="action in actions" type="button" class="btn btn-link panel-action" aria-hidden="true" container="body" v-popover.bottom="'whats up'" data-toggle="button">
            <i :class="iconClass(action.icon)" v-tooltip.top="action.title"></i>
          </a>
        </div> -->

        <!-- <a class="panel-action" aria-hidden="true">
          <i class="zmdi-code-setting"></i>
        </a>
        <a class="panel-action" aria-hidden="true">
          <i class="zmdi zmdi-hc-lg zmdi-refresh-alt"></i>
        </a> -->
        <!-- <slot name="actions"></slot> -->
      <!-- </div>
    </div> -->
    <div :style="bodyStyle" class="panel-body">
      <slot></slot>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      title: {
        type: String,
        default: 'Panel Title',
      },
      actions: {
        type: Array,
        default: null,
      },
      bodyPadding: {
        type: String,
        default: '4px 8px',
      },
    },

    computed: {
      bodyStyle () {
        return {
          padding: this.bodyPadding,
        }
      },
    },
    methods: {
      iconClass (icon) {
        return `zmdi zmdi-hc-lg zmdi-${icon}`
      },
    },
  }
</script>

<style>
  .dropdown-menu {
    position: fixed;
  }
</style>

<style lang="less" scoped>
  @import "~assets/less/variables";

  .panel-flat {
    box-shadow: none;

    .panel-heading {
      position: relative;
      border-bottom: 1px solid #f5f5f5;
    }
  }

  .panel-actions {
    position: absolute;
    top: 50%;
    right: 30px;
    margin: auto;
    transform: translate(0,-50%);


    .panel-action {
      display: inline-block;
      padding: 8px 6px;
      cursor: pointer;
      text-decoration: none;

      .fa, .zmdi {
        color: @gray-light;
        font-weight: 500;
        // .transition(all 0.4s);

        &:hover,
        &.active {
          color: @link-color;
          font-weight: 700;
        }
      }
    }
  }
  @title-font-size: 18px;

  .panel {
    height: 100%;
    overflow: hidden;
    background-color: #fff;
  }

  .panel-body {
    height: calc(~"100% - 60px"); // 50px is the header height!
    overflow: auto;
  }

  .content-section-title {
    line-height: 40px;
  }

  .content-section-heading {
    font-size: @title-font-size;
    font-weight: 500;
    padding: 8px;
    border-bottom: 1px solid #f5f5f5;
    height: 60px;
  }
  .material-icons {
    vertical-align: text-bottom;
    font-size: @title-font-size + 4;
    color: #0c7cd5;
  }

</style>
