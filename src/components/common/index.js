import AceEditor from './AceEditor'
import LogOutput from './LogOutput'
import Panel from './Panel'

function install (Vue) {
  Vue.component('ace-editor', AceEditor)
  Vue.component('log-output', LogOutput)
  Vue.component('panel', Panel)
}

export {
  AceEditor,
  LogOutput,
  Panel,
}

export default {
  install,
}
