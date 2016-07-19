
import popover from './popover'
import tooltip from './tooltip'

function install (Vue) {
  Vue.directive('popover', popover)
  Vue.directive('tooltip', tooltip)
}

export {
  popover,
  tooltip,
}

export default {
  install,
}
