<template>
  <!-- <div
    v-el:modal
    :class="{
      'modal': true,
      'modal-fixed-footer': this.fixedFooter,
      'bottom-sheet': this.bottomSheet,
    }">
    <slot></slot>
  </div> -->
  <div class="modal-mask" v-show="show" transition="modal">
    <div class="modal-wrapper">
      <div class="modal-container">

        <!-- <div class="modal-header">
          <slot name="header">

          </slot>
        </div> -->

        <div class="modal-body">
          <slot>

          </slot>
        </div>

        <!-- <div class="modal-footer">
          <slot name="footer">
            default footer
            <button class="modal-default-button"
              @click="show = false">
              OK
            </button>
          </slot>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      // dismissible: {
      //   type: Boolean,
      //   default: true,
      // },
      // fixedFooter: {
      //   type: Boolean,
      //   default: false
      // },
      // bottomSheet: {
      //   type: Boolean,
      //   default: false
      // },
      // opacity: {
      //   type: Number,
      //   default: 0.5,
      // },
      // inDuration: {
      //   type: Number,
      //   default: 300,
      // },
      // outDuration: {
      //   type: Number,
      //   default: 200,
      // },
      show: {
        type: Boolean,
        // default: false,
        twoWay: true,
      },
    },

    // computed: {
    //   modalOptions () {
    //     return {
    //       dismissible: this.dismissible,
    //       opacity: this.opacity,
    //       in_duration: this.inDuration,
    //       out_duration: this.outDuration,
    //       ready: () => { this.openedModal() },
    //       complete: () => { this.closedModal() }
    //     }
    //   },
    // },
    //
    // events: {
    //   'modal::open' (event) {
    //     console.log('modal::open', event)
    //     this.openModal()
    //
    //   },
    //   'modal::close' (event) {
    //     console.log('modal::Close', event)
    //   }
    // },
    //
    // watch: {
    //   open (newValue) {
    //     newValue
    //       ? this.openModal()
    //       : this.closeModal()
    //   }
    // },
    //
    // methods: {
    //   openModal () {
    //     console.log('openModal')
    //     this.$emit('modal::opening')
    //     this._$modal.openModal(this.modalOptions)
    //   },
    //
    //   openedModal () {
    //     console.log('openedModal')
    //     this.$emit('modal::opened')
    //     this.open = true
    //   },
    //
    //   closeModal () {
    //     console.log('closeModal')
    //     this.$emit('modal::closing')
    //     this._$modal.closeModal()
    //   },
    //
    //   closedModal () {
    //     console.log('closedModal')
    //     this.$emit('modal::closed')
    //     this.open = false
    //   }
    // },
    //
    // ready () {
    //   this._$modal = $(this.$els.modal)
    //
    //   if (this.open) {
    //     this.openModal()
    //   }
    // },

  }
</script>

<style lang="less" scoped>
  // .modal {
  //   z-index: 1003;
  //   display: block;
  // }
  //
  // .overlay {
  //   z-index: 1002;
  //   display: block;
  //   opacity: 0.5;
  // }
  .modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 300px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

/*
 * the following styles are auto-applied to elements with
 * v-transition="modal" when their visiblity is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter, .modal-leave {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}

</style>
