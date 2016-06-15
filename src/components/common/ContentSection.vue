<template>
  <div class="content-section">
    <div class="content-section-title">
      <i class="material-icons">{{ icon }}</i>
      {{ title }}
      <span class="pull-right">
        <slot name="actions"></slot>
      </span>
    </div>
    <div :style="bodyStyle" class="content-section-body">
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
      icon: {
        type: String,
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
      }
    }
  }
</script>

<style lang="less" scoped>
  @title-font-size: 18px;

  .content-section {
    height: 100%;
    overflow: hidden;
    background-color: #fff;
  }

  .content-section-body {
    height: calc(~"100% - 50px"); // 50px is the header height!
    overflow: auto;
  }

  .content-section-title {
    font-size: @title-font-size;
    font-weight: 500;
    padding: 8px;
    border-bottom: 1px solid #f5f5f5;
    height: 50px;
  }
  .material-icons {
    vertical-align: text-bottom;
    font-size: @title-font-size + 4;
    color: #0c7cd5;
  }
</style>
