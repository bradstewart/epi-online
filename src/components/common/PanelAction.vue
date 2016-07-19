<template>
      <div v-if="actions" class="panel-actions">
        <a v-for="action in actions" class="panel-action" aria-hidden="true">
          <i :class="iconClass(action.icon)" v-tooltip.top="action.title"></i>
        </a>
        <!-- <a class="panel-action" aria-hidden="true">
          <i class="zmdi-code-setting"></i>
        </a>
        <a class="panel-action" aria-hidden="true">
          <i class="zmdi zmdi-hc-lg zmdi-refresh-alt"></i>
        </a> -->
        <!-- <slot name="actions"></slot> -->
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

<style lang="less" scoped>
  @import "~assets/less/variables";

  .panel-action {
    display: inline-block;
    padding: 8px 6px;
    cursor: pointer;
    text-decoration: none;

    .fa, .zmdi {
      color: @gray-light;
      font-weight: 500;

      .transition(all 0.4s);
      &:hover {
        color: @link-color;
        font-weight: 700;
      }
    }
  }
</style>
